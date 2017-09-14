# coding=utf-8
import time

from Creature import Creature
from common.events import MsgSCPlayerBorn
from Managers.BackpackManager import BackpackManager
from common.timer import TimerManager
from common.vector import Vector3
from component.AnimationController import AnimationController
from component.SkillHandler import SkillHandler
from component.StateMachine import StateMachine
from component.WeaponHandler import WeaponHandler
from common import DebugAux, conf, Util, GameTime


# class PlayerAttributes(object):
#     def __init__(self, attack, defense, attack_speed, move_speed, make_speed, collect_speed):
#         super(PlayerAttributes, self).__init__()
#         self.attack = attack
#         self.defense = defense
#         self.attack_speed = attack_speed
#         self.move_speed = move_speed
#         self.make_speed = make_speed
#         self.collect_speed = collect_speed


class Player(Creature):
    def __init__(self, client_hid, name, position, rotation, config, group_id, arena):
        super(Player, self).__init__(config['health'], position, rotation, group_id, arena)

        self.client_hid = client_hid
        self.name = name

        # properties
        self.spirit = config['spirit']
        self.attack = config['attack']
        self.defense = config['defense']
        self.body_radius = config['body_radius']

        self.spirit_deduce_time = config['spirit_deduce_time']
        self.spirit_deduce_val = config['spirit_deduce_val']
        self.health_deduce_val = config['blood_deduce_val']
        self.spirit_timer = None

        self.default_move_speed = config['move_speed']
        self.move_velocity = Vector3(0, 0, 0)

        self.accelerate_velocity = Vector3(0, 0, 0)
        self.timer_manager = TimerManager()

        # self.attack_speed = config['attack_speed']
        # self.make_speed = config['make_speed']
        # self.collect_speed = config['collect_speed']

        # components
        self.backpack_manager = BackpackManager(self)

        # skill handler
        self.skill_handler = SkillHandler(self)

        # weapon handler
        self.weapon_handler = WeaponHandler(self)

        # state machine
        self.state_machine = StateMachine(self, 'data.StateMachineData')

        # animation controller
        self.anim_controller = AnimationController('data.animation_data.explorer2_ani',
                                                   'data/animation_data/explorer2.ags')

        # copy
        self.movement_copy = None

        self.is_leave_scene = False

    def add_spirit_deduce_tiemr(self):
        self.spirit_timer = self.timer_manager.add_repeat_timer(self.spirit_deduce_time, self.spirit_auto_deduce)

    def remove_spirit_deduce_timer(self):
        if self.spirit_timer is not None:
            self.timer_manager.cancel(self.spirit_timer)
            self.spirit_timer = None

    def spirit_auto_deduce(self):
        self.spirit_deduce(self.spirit_deduce_val)

    def update(self):
        super(Player, self).update()
        self.move()
        self.timer_manager.scheduler()

    def spirit_update(self):
        pass

    def move(self, detect_collision=conf.DR_DETECT_COLLISION):

        if not conf.DR_OPEN:
            return

        if self.move_velocity.magnitude == 0.0:
            return

        # 预测移动

        next_pos = self.get_position() + Util.calculate_move_distance_with_friction_acceleration(self.move_velocity,
                                                                                                 self.accelerate_velocity,
                                                                                                 GameTime.delta_time)

        if detect_collision:
            # 检查移动是否合法，预测移动不进行人物之间的碰撞检测，防止卡住
            fixed_dst_pos = self.move_legal(self.get_position(), next_pos)

            if fixed_dst_pos is not None:
                self.set_position(fixed_dst_pos)
        else:
            self.set_position(next_pos)

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
                if (src_pos - other.get_position()).magnitude < self.body_radius * 2:
                    # 若已经处于碰在一起的状态，不再检测碰撞
                    continue
                if (dst_pos - other.get_position()).magnitude < self.body_radius * 2:
                    return None

        # 允许切向量方向的滑动，返回修正后的目标位置
        fixed_pos = self.arena.universe.approach(src_pos, dst_pos)
        return Vector3(fixed_pos.x, fixed_pos.y, fixed_pos.z)

    def add_weapon(self, wid):
        self.weapon_handler.add_weapon(wid)

    def debug_base_attack(self):
        return object.__getattribute__(self, "attack")

    def debug_weapon_attack(self):
        return self.backpack_manager.debug_weapon_attack()

    def debug_base_defense(self):
        return self.backpack_manager.debug_defense()

    def generate_born_msg(self, send_to_others):
        return MsgSCPlayerBorn(self.entity_id, send_to_others, self.name, self.health, self.position.x,
                               self.position.y, self.position.z, self.rotation.x, self.rotation.y, self.rotation.z)

    def set_leave_scene(self):
        self.is_leave_scene = True

    def is_dead(self):
        if self.is_leave_scene:
            return True
        return self.health <= 0

    def add_spirit(self, val, spirit):
        self.spirit = self.spirit + int(val * spirit)
        if self.spirit > 100:
            self.spirit = 100

    def set_position(self, pos):
        if self.is_dead():
            return
        super(Player, self).set_position(pos)

    def set_rotation(self, rot):
        if self.is_dead():
            return
        super(Player, self).set_rotation(rot)

    def get_backpack_syn_message(self):
        from common.events import MsgSCBackpackSyn

        msg = self.backpack_manager.generate_backpack_syn_message_ex()
        data = msg.marshal()

        cc = MsgSCBackpackSyn()
        cc.unmarshal(data)

        self.backpack_manager.parse_backpack_syn_message_ex(cc)

        return msg

    def get_attack_value(self, weapon_deduce=True):
        if hasattr(self, "attack") is False:
            return

        if weapon_deduce is True:
            DebugAux.Log("[server] [player] True")
            return self.attack + self.backpack_manager.get_attack()
        else:
            DebugAux.Log("[server] [player] False")
            return self.attack + self.backpack_manager.debug_weapon_attack()

    def __del__(self):
        if self.spirit_timer is not None:
            self.timer_manager.cancel(self.spirit_timer)

    def save_current_movement_state(self):
        self.movement_copy = {'p': self.get_position(),
                              'v': self.get_move_velocity(),
                              'a': self.get_accelerate_velocity(),
                              'states': self.state_machine.pack_all_states(),
                              'health': self.health,
                              }

    def recover_movement_state(self):
        self.set_position(self.movement_copy['p'])
        self.set_move_velocity(self.movement_copy['v'])
        self.set_accelerate_velocity(self.movement_copy['a'])
        self.state_machine.set_all_states(self.movement_copy['states'])
        self.health = self.movement_copy['health']

    def check_state(self, state_name):
        return self.state_machine.cur_state == state_name

    def in_attack_range(self, other, dis):
        """
        判断pos是否在攻击范围内，在范围内需要自动锁定被攻击者
        圆形攻击范围
        """
        if (self.get_position() - other.get_position()).magnitude > dis:
            return None
        return abs(other.get_rotation().y - self.rotation.y)

    def attack_face_to(self, dis):
        """
        寻找范围内一个攻击角度最小的目标，并面向它
        :return:
        """
        min_angle = None
        target = None
        for p in self.arena.client_id_to_player_map.itervalues():
            if p is None or p.is_dead() or p.entity_id == self.entity_id:
                continue
            angle = self.in_attack_range(p, dis)
            if angle is None:
                continue
            if min_angle is None or abs(angle) < abs(min_angle):
                min_angle = angle
                target = p
        if min_angle is not None:
            self.look_at_position(target.get_position())
