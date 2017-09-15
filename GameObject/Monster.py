# coding=utf-8
from copy import copy

import behavior
import time

from Configuration import MonsterDB
from Creature import Creature
from BPItemObject import BPItemObject
from common import Util, GameTime, conf, DebugAux
from common.events import MsgSCMonsterMove, MsgSCMonsterAttack, MsgSCMapItemDrop
from common.vector import Vector3
from component.AnimationController import AnimationController
from component.SkillHandler import SkillHandler
from component.StateMachine import StateMachine


class MovementState(object):
    def __init__(self):
        super(MovementState, self).__init__()
        self.position = None
        self.rotation = None
        self.velocity = None
        self.acceleration = None
        self.state_names = None

    def set(self, pos, rot, v, a, state_names):
        self.position = pos
        self.rotation = rot
        self.velocity = v
        self.acceleration = a
        self.state_names = state_names

    def update_remote_position(self, delta_time):
        """
        计算远程客户端位置
        """
        if self.velocity.magnitude == 0:
            return

        self.position += Util.calculate_move_distance_with_friction_acceleration(self.velocity,
                                                                                 self.acceleration, delta_time)

        if self.acceleration.magnitude * delta_time >= self.velocity.magnitude:
            self.velocity = Vector3(0, 0, 0)
        else:
            self.velocity += self.acceleration * delta_time


class Monster(Creature):
    def __init__(self, ID, health, position, rotation, group_id, arena):
        super(Monster, self).__init__(health, position, rotation, group_id, arena)
        self.ID = ID
        data = MonsterDB.get_info_by_ID(ID)
        self.unlock_distance = data["unlock_distance"]
        self.attack = data['attack']
        self.body_radius = data['body_radius']

        self.ai_tree = None
        self.blackboard = None
        self.target_player_client_hid = -1
        self.born_position = position

        self.default_move_speed = data['move_speed']
        self.move_velocity = Vector3(0, 0, 0)
        self.accelerate_velocity = Vector3(0, 0, 0)

        # skill handler
        self.skill_handler = SkillHandler(self)
        self.skills = data.get('skill')
        if self.skills is not None:
            self.skill_handler.add_skills(self.skills.keys())

        # state machine
        self.state_machine = StateMachine(self, 'data.StateMachineData')

        model_name = data['model_name'].split('/')[-1].split('.')[0]
        # animation controller
        self.anim_controller = AnimationController('data.animation_data.' + model_name + '_ani',
                                                   'data/animation_data/' + model_name + '.ags', down_anim='die',
                                                   up_anim=None)
        # copy
        self.movement_copy = None

        # send movement message
        self.last_send_movement_state = MovementState()
        self.set_last_send_movement_state()

        # hit提前预判
        self.hit_predict_time = 0.1

        #
        self.is_attacking = False
        self.attack_start_time = None
        self.attack_time = None
        self.attack_start_to_move_time = None
        self.attack_move_data = {}
        self.attack_start_to_hit_time = None
        self.attack_hit_data = {}

    def update(self):
        if self.check_state(conf.STATE_ATTACK):
            self.do_attack_things()

        super(Monster, self).update()

        self.move()
        self.last_send_movement_state.update_remote_position(GameTime.delta_time)  # 更新远程位置
        self.try_send_move_msg()  # 对比当前位置状态与远程位置状态，满足条件时发送状态同步消息

        if self.check_state(conf.STATE_IDLE) or self.check_state(conf.STATE_MOVE):
            self.ai_tree.tick({}, self.blackboard)

    def test_attack(self):
        if self.skills is None:
            return
        sid = self.skills.keys()[0]
        if self.check_state(conf.STATE_IDLE) or self.check_state(conf.STATE_MOVE):
            for gid, group in self.arena.group_map.iteritems():
                if gid == self.get_group_id():
                    continue
                for p in group:
                    if (p.get_position() - self.get_position()).magnitude < 150:
                        self.input_attack_command(sid)

    def input_move_command(self, direct):
        self.set_move_velocity(direct * self.default_move_speed)
        self.accelerate_velocity = Vector3(0, 0, 0)

    def input_attack_command(self, sid):
        """
        发出攻击命令，设置定时器，距离hit点一定时间计算受击目标
        """
        pos = self.get_position()
        msg = MsgSCMonsterAttack(self.entity_id, pos.x, pos.y, pos.z, sid)
        self.arena.broadcast(msg)

        start_node = self.skill_handler.get_skill_node_config(sid, 'start')
        act_node_config = self.skill_handler.get_skill_node_config(sid, start_node[0])  # 默认只有一个动作
        act_ani_name = act_node_config.get('args')[0]

        move_node_name = None
        hit_node_name = None  # 默认只有一个hit事件
        hit_node_tag = None

        nexts = act_node_config.get('next')
        for node_type, next_nodes in nexts.iteritems():
            if node_type == 'tag':
                for tag, args in next_nodes.iteritems():
                    if tag == 'mov':
                        move_node_name = args[0]
                    elif tag.startswith('hit'):
                        hit_node_tag = tag
                        hit_node_name = args[0]

        act_time = self.anim_controller.get_anim_time(act_ani_name) / 1000.0
        move_start_time = None
        move_data = None
        hit_start_time = None
        hit_data = None

        act_events = self.anim_controller.get_anim_events(act_ani_name)
        for e in act_events:
            tim = e[1] / 1000.0
            if e[0] == 'mov':
                move_start_time = tim
                move_data = {'sid': sid, 'node_name': move_node_name}
            elif e[0].startswith('hit'):
                hit_start_time = tim - self.hit_predict_time
                hit_data = {'sid': sid, 'node_name': hit_node_name, 'tag': hit_node_tag, 'idx': 1, 'hit_time': self.hit_predict_time}

        self.state_machine.change_state(conf.STATE_ATTACK)
        self.enter_attack_state(act_time, move_start_time, move_data, hit_start_time, hit_data)

    def move(self):

        if self.move_velocity.magnitude == 0.0:
            return

        # 预测移动

        next_pos = self.get_position() + Util.calculate_move_distance_with_friction_acceleration(self.move_velocity,
                                                                                                 self.accelerate_velocity,
                                                                                                 GameTime.delta_time)

        # 检查移动是否合法
        fixed_dst_pos = self.move_legal(self.get_position(), next_pos)

        if fixed_dst_pos is not None:
            self.set_position(fixed_dst_pos)

        # 更新移动速度
        self.move_velocity = Util.calculate_velocity_with_friction_acceleration(self.move_velocity,
                                                                                self.accelerate_velocity,
                                                                                GameTime.delta_time)

    def move_legal(self, src_pos, dst_pos, check_player_collision=True):
        """
        移动是否合法，（1） 地图边缘（2） 其他玩家碰撞
        """
        if check_player_collision:
            for other in self.arena.client_id_to_player_map.itervalues():
                if other is None or other == self or other.is_dead():
                    continue
                if (src_pos - other.get_position()).magnitude < self.body_radius + other.body_radius:
                    # 若已经处于碰在一起的状态，不再检测碰撞
                    continue
                if (dst_pos - other.get_position()).magnitude < self.body_radius + other.body_radius:
                    return None

        # 允许切向量方向的滑动，返回修正后的目标位置
        fixed_pos = self.arena.universe.approach(src_pos, dst_pos)
        return Vector3(fixed_pos.x, fixed_pos.y, fixed_pos.z)

    def is_dead(self):
        return self.health <= 0

    def need_to_send_movement_msg(self):
        """
        是否需要发送移动消息
        """

        # 受击时不发送消息
        if self.check_state(conf.STATE_LIEDOWN) or self.check_state(conf.STATE_STIFFNESS):
            return False

        # rotation不一致需要马上发消息
        if not (self.last_send_movement_state.rotation - self.get_rotation()).magnitude == 0:
            return True

        # 若状态改变也要发消息，主要用于碰撞时跑步位移不变的情况
        if self.state_machine.pack_all_states() != self.last_send_movement_state.state_names:
            return True

        max_diff = 0.1

        # 位置差距较大时需要发送同步消息
        remote_pos = self.last_send_movement_state.position
        if (self.position - remote_pos).magnitude > max_diff:
            return True

        return False

    def try_send_move_msg(self, force=False):

        # 发送移动消息
        if not force and not self.need_to_send_movement_msg():
            return

        pos = self.get_position()
        rot = self.get_rotation()

        v = self.get_move_velocity()
        a = self.get_accelerate_velocity()

        # print 'send move msg', pos, ' ', v, ' ', a

        msg = MsgSCMonsterMove(self.entity_id, pos.x, pos.z, rot.y, v.x, v.z, a.x, a.z)
        self.arena.broadcast(msg)

        # 记录上一次发送的状态消息
        self.set_last_send_movement_state()

    def set_last_send_movement_state(self):
        self.last_send_movement_state.set(self.get_position(), self.get_rotation(), self.get_move_velocity(),
                                          self.get_accelerate_velocity(), self.state_machine.pack_all_states())

    def get_attack_value(self):
        return self.attack

    def health_damage(self, val, attack_percent):
        """
        :param attack_percent:
        :param val: damage value
        :return: live->true, die->false
        """

        if val < 0:
            val = 0

        val = val * attack_percent
        if val < 0:
            val = 0

        self.health -= int(val)

        if self.health <= 0:
            self.health = 0
            self.drop_materials()

    def drop_materials(self):
        data = MonsterDB.get_info_by_ID(self.ID)
        drop_items = data['drop_items']
        for id, num in drop_items.items():
            for k in xrange(0, num):
                cell = BPItemObject(id, 1)
                self.arena.universe.drop(self.position, cell)
                drop_msg = MsgSCMapItemDrop(self.position.x, self.position.y, self.position.z, cell.item)
                self.arena.broadcast(drop_msg)

    def enter_attack_state(self, attack_time, move_time, move_data, hit_time, hit_data):
        self.attack_start_time = time.time()
        self.attack_time = attack_time
        self.attack_start_to_move_time = move_time
        self.attack_move_data = move_data
        self.attack_start_to_hit_time = hit_time
        self.attack_hit_data = hit_data

    def do_attack_things(self):
        t = time.time() - self.attack_start_time

        if t > self.attack_time:
            self.state_machine.change_state(conf.STATE_IDLE)
            return
        # attack hit
        if self.attack_start_to_hit_time is not None and t > self.attack_start_to_hit_time:
            self.skill_handler.handle_attack_hit(self.attack_hit_data['sid'], self.attack_hit_data['node_name'],
                                                 self.attack_hit_data['tag'], self.attack_hit_data['idx'],
                                                 self.attack_hit_data['hit_time'])
            self.attack_start_to_hit_time = None
        # attack move
        if self.attack_start_to_move_time is not None and t > self.attack_start_to_move_time:
            self.skill_handler.parse_move_node(self.attack_move_data['sid'], self.attack_move_data['node_name'])
            self.attack_start_to_move_time = None
    '''
    **************************************AI 辅助函数***********************************************begin
    '''
    def route(self):
        if self.target_player_client_hid in self.arena.client_id_to_player_map:
            return self.arena.client_id_to_player_map[self.target_player_client_hid].position,1
        else:
            data = MonsterDB.get_info_by_ID(self.ID)
            r_min, r_max = data['walk_distance']
            target_pos = self.arena.universe.get_patrol_position(self.born_position, r_min, r_max)
            if target_pos:
                return target_pos, 0
            else:
                return self.born_position, 0

    def has_target(self):
        if self.target_player_client_hid in self.arena.client_id_to_player_map:
            return True
        else:
            return False

    def get_current_position(self):
        return copy(self.position)

    def idle(self):
        direction = Vector3(0,0,0)
        self.input_move_command(direction)
        DebugAux.Log("AI setting idle")

    def moving(self, pos):
        direction = pos - self.position
        try:
            direction = direction.normalize
        except:
            direction = Vector3(0,0,0)

        self.input_move_command(direction)

        if self.target_player_client_hid not in self.arena.client_id_to_player_map:
            self.find_nearest_player()

    def is_attack_available(self):
        if self.target_player_client_hid in self.arena.client_id_to_player_map:
            vec = self.arena.client_id_to_player_map[self.target_player_client_hid].position - self.position
            if vec.magnitude < 150:
                return True
            else:
                return False
        else:
            return False

    def find_nearest_player(self):
        info = MonsterDB.get_info_by_ID(self.ID)
        lock_distance = info["lock_distance"]
        for player in self.arena.client_id_to_player_map.itervalues():
            vec = player.position-self.position
            if vec.magnitude < lock_distance and player.check_state(conf.STATE_DEFENCE) is True:
                self.set_player_target(player.client_hid)
                break
            elif vec.magnitude < lock_distance:
                self.set_player_target(player.client_hid)
                break

    def attack_action(self):
        from universe.misc import PseudoRandom

        info = MonsterDB.get_info_by_ID(self.ID)

        if "skill" in info.keys():
            skill = info["skill"]
        else:
            return

        random = PseudoRandom()
        cmd = random.weight_choice(skill.items(), value=lambda x: x[0], weight=lambda x: x[1])
        self.input_attack_command(cmd)

    def set_player_target(self, client_hid):
        if self.target_player_client_hid not in self.arena.client_id_to_player_map:
            self.target_player_client_hid = client_hid

    def set_ai_behavior_tree(self, ai_tree):
        self.ai_tree = ai_tree
        self.ai_tree.host = self

        idle_node = self.ai_tree.get_node_by_title("Idle")

        idle_node.set_time(7)

        self.blackboard = behavior.Blackboard()

    def unlock_player_target(self):
        self.target_player_client_hid = None

    '''
    **************************************AI 辅助函数***********************************************end
    '''