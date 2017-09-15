# coding=utf-8
import importlib
import random

import time

import behavior
from AI.monster_ai import AI_Lib
from GameObject.Bullet import Bullet
from GameObject.Monster import Monster
from Managers.BackpackManager import BackpackManager
from common import Util
from common.events import MsgSCPlayerReapHit, MsgSCWeaponUninstall, MsgSCPlayerHit, MsgSCBulletSpawn, MsgSCBulletHit, \
    MsgSCWeaponDeduce, MsgSCSpiritBloodSyn, MsgSCGameWin, MsgSCMonsterBorn, MsgSCGameWinCountDown, MsgSCMonsterWaitTime, \
    MsgSCMonsterAlertTime
from common.timer import TimerManager
import universe
from common.vector import Vector3
from common import EventManager
from common import conf
from common import DebugAux
from GameObject.GameObject import GameObject
from Managers.MonsterManager import MonsterManager
from Configuration import MonsterDB, MonsterRefresh


class Arena(object):
    def __init__(self, host, arena_conf_filename, player_conf_filename, game_type=0):
        '''
        :param host:
        :param arena_conf_filename:
        :param player_conf_filename:
        :param arena_type: single 0, normal 1, battle 2
        '''
        super(Arena, self).__init__()

        self.host = host
        self.game_type = game_type

        self.client_id_to_player_map = {}
        self.username_to_invalid_player_map = {}
        self.username_to_user = {}
        self.entity_id_to_monster_map = {}

        self.timeManager = TimerManager()
        self.monster_manager = MonsterManager(game_type)

        # arena configuration
        self.arena_conf = importlib.import_module(arena_conf_filename).configuration
        self.player_conf = importlib.import_module(player_conf_filename).explorer

        # game status
        self.is_game_start = False
        self.is_game_stop = False

        # universe object [Not Implemented]
        self.client_id_finished_map = {}
        import uuid
        self.universe = universe.get(id=uuid.uuid1(), new=True)

        # bullets
        self.bullets = {}

        # group
        self.group_num = 0
        self.group_map = {  # group_id -> []
            999: [],  # monster
        }

    # arena tick
    def tick(self):
        self.timeManager.scheduler()

        dead_player_list = {}
        # players
        for hid, player in self.client_id_to_player_map.iteritems():
            if player is None:
                dead_player_list[hid] = player
            if player.is_dead():
                dead_player_list[hid] = player
                self.group_map[player.group_id].remove(player)
            else:
                player.update()

        for hid, player in dead_player_list.iteritems():
            del self.client_id_to_player_map[hid]
            if player is not None:
                self.player_quit(hid, None)
            DebugAux.Log('tick ',self.client_id_to_player_map.keys())

        # monsters
        del_mids = []
        for mid, monster in self.entity_id_to_monster_map.iteritems():
            if monster is None:
                del_mids.append(mid)
            elif monster.is_dead():
                del_mids.append(mid)
                self.group_map[monster.group_id].remove(monster)
            else:
                monster.update()

        for mid in del_mids:
            del self.entity_id_to_monster_map[mid]

        # bullets
        dead_bullets = []
        for bid, bullet in self.bullets.iteritems():
            bullet.update()
            if bullet.is_dead():
                dead_bullets.append(bid)
        for bid in dead_bullets:
            del self.bullets[bid]

        if self.monster_manager is not None:
            self.monster_manager.tick()

    def send_map_seed_to_all_clients(self):
        from common.events import MsgSCMapLoad
        import sys
        seed = random.randint(0, sys.maxint)
        msg = MsgSCMapLoad(seed)
        data = msg.marshal()

        for _, user in self.username_to_user.items():
            self.host.sendClient(user.client_hid, data)

        self.universe.seed(seed)
        self.universe.create()

    def init_game(self, users):
        from GameObject.Player import Player
        self.username_to_user = users

        # send universe seed to all clients
        self.send_map_seed_to_all_clients()

        if conf.DEBUG_SAME_POSITION:
            x = 0

        for hid, user in self.username_to_user.items():
            if conf.DEBUG_SAME_POSITION:
                born_position = Vector3(x, 5, 0)
                x += 200
            else:
                blocks = ["grass", "withered", "marsh"]
                born_position = Vector3(self.universe.get_born_position(random.choice(blocks)))
            born_rotation = Vector3(0, 0, 0)
            player = Player(user.client_hid, user.username, born_position,
                            born_rotation, self.player_conf, self.group_num, self)

            self.client_id_to_player_map[user.client_hid] = player
            if self.group_num in self.group_map:
                self.group_map[self.group_num].append(player)
            else:
                self.group_map[self.group_num] = [player, ]
            if self.game_type != 2:
                self.group_num += 1

        DebugAux.Log(self.client_id_to_player_map.keys())
        # Send player born message
        self.send_player_born_msg()

        # waiting the clients to load universe and resource
        self.timeManager.add_timer(300, self.start_game_count_down)

    def stop_game(self):
        # 清空游戏

        self.is_game_start = False
        self.is_game_stop = True

        # remove various listener
        EventManager.remove_observer(conf.MSG_CS_PLAYER_DROP, self.player_drop)
        EventManager.remove_observer(conf.MSG_CS_WEAPON_INSTALL, self.weapon_install)
        EventManager.remove_observer(conf.MSG_CS_WEAPON_UNINSTALL, self.weapon_uninstall)
        EventManager.remove_observer(conf.MSG_CS_ARMOR_INSTALL, self.armor_install)
        EventManager.remove_observer(conf.MSG_CS_HAT_INSTALL, self.hat_install)
        EventManager.remove_observer(conf.MSG_CS_MAKE_REQUEST, self.handle_make_request)
        EventManager.remove_observer(conf.MSG_CS_WEAPON_ACTIVE, self.handle_weapon_active)
        EventManager.remove_observer(conf.MSG_CS_GM_BP_CMD, self.gm_backpack_cmd)

        self._release_all_player_listeners()
        self._remove_spirit_deduce_timer()

        self.monster_manager.stop_game()
        self.monster_manager.add_listener(MonsterManager.GAME_WIN_LISTENER, self.handle_game_win)
        self.monster_manager.add_listener(MonsterManager.GAME_WIN_COUNT_DOWN_LISTENER, self.handle_game_win_count_down)
        self.monster_manager.add_listener(MonsterManager.MONSTER_REMIND_LISTENER, self.handle_monster_remind)
        self.monster_manager.add_listener(MonsterManager.MONSTER_REMIND_RED_LISTENER, self.handle_monster_red_alert)
        self.monster_manager.add_listener(MonsterManager.MONSTER_COMING_LISTENER, self.handle_monster_coming)

    def start_game(self):
        self.is_game_start = True
        self.is_game_stop = False

        # update arena/(1000/30ms)
        # self.timeManager.add_repeat_timer(1000 / 30, self.update_arena)

        # add various listener
        EventManager.add_observer(conf.MSG_CS_PLAYER_DROP, self.player_drop)
        EventManager.add_observer(conf.MSG_CS_WEAPON_INSTALL, self.weapon_install)
        EventManager.add_observer(conf.MSG_CS_WEAPON_UNINSTALL, self.weapon_uninstall)
        EventManager.add_observer(conf.MSG_CS_ARMOR_INSTALL, self.armor_install)
        EventManager.add_observer(conf.MSG_CS_HAT_INSTALL, self.hat_install)
        EventManager.add_observer(conf.MSG_CS_MAKE_REQUEST, self.handle_make_request)
        EventManager.add_observer(conf.MSG_CS_WEAPON_ACTIVE, self.handle_weapon_active)
        EventManager.add_observer(conf.MSG_CS_GM_BP_CMD, self.gm_backpack_cmd)

        self._init_all_player_listeners()
        self._add_spirit_deduce_timer()

        self.monster_manager.add_listener(MonsterManager.GAME_WIN_LISTENER, self.handle_game_win)
        self.monster_manager.add_listener(MonsterManager.GAME_WIN_COUNT_DOWN_LISTENER, self.handle_game_win_count_down)
        self.monster_manager.add_listener(MonsterManager.MONSTER_REMIND_LISTENER, self.handle_monster_remind)
        self.monster_manager.add_listener(MonsterManager.MONSTER_REMIND_RED_LISTENER, self.handle_monster_red_alert)
        self.monster_manager.add_listener(MonsterManager.MONSTER_COMING_LISTENER, self.handle_monster_coming)

        self.monster_manager.start_game()

        self._generate_map_monster()

        # if conf.DEBUG_SAME_POSITION:
        #     born_pos = Vector3(-200, 5, 0)
        #     monster = Monster(100, 100, born_pos, Vector3(0, 0, 0), 999, self)
        #
        #     btree = behavior.BehaviorTree()
        #     btree.load(AI_Lib.ChaseMonster)
        #
        #     monster.set_ai_behavior_tree(btree)
        #
        #     self.entity_id_to_monster_map[monster.entity_id] = monster
        #     self.group_map[monster.group_id].append(monster)
        #     msg = MsgSCMonsterBorn(monster.entity_id, monster.ID, monster.health, born_pos.x, born_pos.y, born_pos.z,
        #                            monster.group_id)
        #     self.broadcast(msg)

    def _generate_map_monster(self):
        if self.game_type == 0:
            self.config = MonsterRefresh.single_model
        elif self.game_type == 1:
            self.config = MonsterRefresh.normal_model
        elif self.game_type == 2:
            self.config = MonsterRefresh.battle_model
        else:
            raise "[error] game type error"

        for cell in self.config["map_monster"]:
            for index in xrange(0, cell["total_num"]):
                info = MonsterDB.get_info_by_ID(cell["ID"])
                born_block = cell["refresh_location"]
                born_pos = Vector3(self.universe.get_born_position(born_block))

                btree = behavior.BehaviorTree()
                btree.load(AI_Lib.ChaseMonster)

                monster = Monster(cell["ID"], info["health"], born_pos, Vector3(), 999, self)
                monster.set_ai_behavior_tree(btree)

                self.entity_id_to_monster_map[monster.entity_id] = monster
                self.group_map[monster.group_id].append(monster)
                msg = MsgSCMonsterBorn(monster.entity_id, monster.ID, monster.health, born_pos.x, born_pos.y,
                                       born_pos.z, monster.group_id)
                self.broadcast(msg)

    def _init_all_player_listeners(self):
        for player in self.client_id_to_player_map.itervalues():
            # add backpack change listener
            # 1. install and uninstall event
            # 2. backpack quantity change event
            player.backpack_manager.add_listener(BackpackManager.BP_INSTALL_UNINSTALL_LISTENER,
                                                 self.player_bp_install_uninstall_handler)
            player.backpack_manager.add_listener(BackpackManager.BP_QUANTITY_CHANGE_LISTENER,
                                                 self.player_bp_weapon_deduce_handler)
            player.backpack_manager.add_listener(BackpackManager.BP_BRING_IN_LISTENER,
                                                 self.player_bing_in_handler)
            player.backpack_manager.add_listener(BackpackManager.BP_TAKE_AWAY_LISTENER,
                                                 self.player_bp_take_away_handler)

            # add game object event listener [player]
            player.add_listener(GameObject.EVENT_DEAD, self.player_dead)
            player.add_listener(GameObject.EVENT_SPIRIT, self.player_spirit_change)

    def _release_all_player_listeners(self):
        for player in self.client_id_to_player_map.itervalues():
            # add backpack change listener
            # 1. install and uninstall event
            # 2. backpack quantity change event
            player.backpack_manager.remove_listener(BackpackManager.BP_INSTALL_UNINSTALL_LISTENER,
                                                    self.player_bp_install_uninstall_handler)
            player.backpack_manager.remove_listener(BackpackManager.BP_QUANTITY_CHANGE_LISTENER,
                                                    self.player_bp_weapon_deduce_handler)
            player.backpack_manager.remove_listener(BackpackManager.BP_BRING_IN_LISTENER,
                                                    self.player_bing_in_handler)
            player.backpack_manager.remove_listener(BackpackManager.BP_TAKE_AWAY_LISTENER,
                                                    self.player_bp_take_away_handler)

            # add game object event listener [player]
            player.remove_listener(GameObject.EVENT_DEAD, self.player_dead)
            player.remove_listener(GameObject.EVENT_SPIRIT, self.player_spirit_change)

    def _add_spirit_deduce_timer(self):
        for player in self.client_id_to_player_map.itervalues():
            player.add_spirit_deduce_tiemr()

    def _remove_spirit_deduce_timer(self):
        for player in self.client_id_to_player_map.itervalues():
            player.remove_spirit_deduce_timer()

    # def update_arena(self):
    #     pass

    def broadcast(self, msg, not_send=None):
        for player in self.client_id_to_player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def player_quit(self, client_hid, msg):
        from common.events import MsgSCPlayerLeave

        if client_hid not in self.client_id_to_player_map:
            return

        DebugAux.Log("[server] [Arena] receive player quit [][][][]")

        player = self.client_id_to_player_map[client_hid]
        player.remove_spirit_deduce_timer()

        del self.client_id_to_player_map[client_hid]
        for user in self.username_to_user.itervalues():
            if user.client_hid == client_hid:
                del self.username_to_user[user.username]
                break

        msg = MsgSCPlayerLeave(player.entity_id)
        self.broadcast(msg)

        if len(self.client_id_to_player_map) <= 0:
            self.stop_game()

        DebugAux.Log(self.client_id_to_player_map.keys())

    def player_leave(self, client_hid):
        from common.events import MsgSCPlayerLeave
        # player leave the arena
        if self.client_id_to_player_map.has_key(client_hid) is True:
            player = self.client_id_to_player_map[client_hid]
            player.remove_spirit_deduce_timer()
            self.username_to_invalid_player_map[player.name] = player
            del self.client_id_to_player_map[client_hid]
            DebugAux.Log("Red alert : Server broadcast player leave message [][][][]")
            msg = MsgSCPlayerLeave(player.entity_id)
            self.broadcast(msg)

        if len(self.client_id_to_player_map) <= 0:
            self.stop_game()

        DebugAux.Log("player leave",self.client_id_to_player_map.keys())

    def player_enter_again(self, user):
        '''
        :param user: user data
        :return: None

        @log:
             1. after some of the universe items were destroyed by players.sending universe seed to regenerate universe is not right.
                return
        '''

        return

        from common.events import MsgSCMapLoad

        # user is not in this arena
        if self.username_to_user.has_key(user.username) is False:
            return

        if self.username_to_invalid_player_map.has_key(user.username) is False:
            return

        player = self.username_to_invalid_player_map[user.username]
        del self.username_to_invalid_player_map[user.username]
        self.client_id_to_player_map[user.client_hid] = player

        # notify client to load universe
        msg = MsgSCMapLoad(-1)  # Not implemented -1 error
        data = msg.marshal()
        self.host.sendClient(user.client_hid, data)

        # send born msg to this client and other clients
        msg = player.generate_born_msg(0)  # send to itself
        self.host.sendClient(player.client_hid, msg.marshal())
        msg = player.generate_born_msg(1)  # send to others
        self.broadcast(msg, not_send=player)

        # send other players born message to this client
        for oplayer in self.client_id_to_player_map.itervalues():
            if oplayer is not player:
                msg = oplayer.generate_born_msg(1)
                self.host.sendClient(player.client_hid, msg.marshal())

    def send_player_born_msg(self):
        DebugAux.Log("send born msg")
        for player in self.client_id_to_player_map.itervalues():
            msg = player.generate_born_msg(0)  # send to itself
            self.host.sendClient(player.client_hid, msg.marshal())
            self.send_backpack_syn_message(player.client_hid)
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

        self._init_all_player_weapon()

    def _init_all_player_weapon(self):
        for hid, player in self.client_id_to_player_map.items():
            self._init_weapon_per_player(player)

    def _init_weapon_per_player(self, player):
        from common.events import MsgSCWeaponInstall
        active_weapon = player.backpack_manager.get_active_weapon()
        if active_weapon is not None:
            msg = MsgSCWeaponInstall(player.entity_id, active_weapon.ID)
            self.broadcast(msg)

        if player.backpack_manager.armor is not None:
            msg = MsgSCWeaponInstall(player.entity_id, player.backpack_manager.armor.ID)
            self.broadcast(msg)

        if player.backpack_manager.hat is not None:
            msg = MsgSCWeaponInstall(player.entity_id, player.backpack_manager.hat.ID)
            self.broadcast(msg)

    def handle_player_move(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]

        if player.is_dead():
            return

        state = msg.state_names.split('|')[0]

        if player.check_state(conf.STATE_LIEDOWN) and state != conf.STATE_LIEDOWN:
            return

        if player.check_state(conf.STATE_STIFFNESS) and state != conf.STATE_STIFFNESS:
            return

        # 需要检测移动的合法性，包括地图边界判断和碰撞检测, FIX ME !!!
        player.sync_position_rotation(msg)

        player.set_move_velocity(Vector3(msg.vx, msg.vy, msg.vz))
        player.set_accelerate_velocity(Vector3(msg.ax, msg.ay, msg.az))

        if player.check_state(conf.STATE_LIEDOWN) or player.check_state(conf.STATE_STIFFNESS):
            # 受击或摔倒的时候不接收移动消息，等客户端玩家受击完之后发送受击完成消息，改变状态才能同步移动消息
            return

        player.state_machine.set_all_states(msg.state_names)

        # broadcast move info to other player
        if conf.DEBUG_SYNC_OPEN:
            self.broadcast(msg)
        else:
            self.broadcast(msg, not_send=player)

    def handle_player_hit_recover(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]

        if player.is_dead():
            return

        if player.check_state(conf.STATE_LIEDOWN) and msg.is_lie_down:
            player.state_machine.change_state(conf.STATE_IDLE)
        elif player.check_state(conf.STATE_STIFFNESS) and not msg.is_lie_down:
            player.state_machine.change_state(conf.STATE_IDLE)

    def handle_player_position(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]

        if player.is_dead():
            return

        # 需要检测移动的合法性，包括地图边界判断和碰撞检测, FIX ME !!!

        player.set_position([msg.px, 5.0, msg.pz])
        player.set_rotation([0, msg.ry, 0])

        # broadcast move info to other player
        if conf.DEBUG_SYNC_OPEN:
            self.broadcast(msg)
        else:
            self.broadcast(msg, not_send=player)

    def handle_player_attack(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        if player.check_state(conf.STATE_LIEDOWN) or player.check_state(conf.STATE_STIFFNESS):
            # 受击或摔倒的时候不接收移动消息，等客户端玩家受击完之后发送受击完成消息，改变状态才能同步移动消息
            return

        player.sync_position_rotation(msg)

        DebugAux.Log("player attack")

        # broadcast move info to other player
        if conf.DEBUG_SYNC_OPEN:
            self.broadcast(msg)
        else:
            self.broadcast(msg, not_send=player)

        # 武器消耗，标枪没有命中强制使用一次武器。
        #active_weapon = player.backpack_manager.get_active_weapon()
        #if active_weapon is not None and active_weapon.pile_bool is True and msg.button_down is False:
            #player.get_attack_value()
            # active_weapon.num -= 1
            # die_list = player.backpack_manager.inquire_weapon_die()
            # for id in die_list:
            # msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
            # self.broadcast(msg_tmp)

            # $self.send_backpack_syn_message(client_hid)

    def handle_player_run_act_node(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        attacker = self.client_id_to_player_map[client_hid]
        if attacker.is_dead():
            return

        if attacker.check_state(conf.STATE_LIEDOWN) or attacker.check_state(conf.STATE_STIFFNESS):
            # 受击或摔倒的时候不接收移动消息，等客户端玩家受击完之后发送受击完成消息，改变状态才能同步移动消息
            return

        DebugAux.Log("player run act node")

        # 保存当前位置信息
        for player in self.client_id_to_player_map.itervalues():
            if player is None or player.is_dead():
                continue
            player.save_current_movement_state()

        # 进行模拟
        act_node_config = attacker.skill_handler.get_skill_node_config(msg.skill_id, msg.node_name)
        act_ani_name = act_node_config.get('args')[0]

        move_node = None
        hit_nodes = {}

        nexts = act_node_config.get('next')
        for node_type, next_nodes in nexts.iteritems():
            if node_type == 'tag':
                for tag, args in next_nodes.iteritems():
                    if tag == 'mov':
                        move_node = args[0]
                    elif tag.startswith('hit'):
                        hit_nodes[tag] = args[0]

        act_events = attacker.anim_controller.get_anim_events(act_ani_name)
        idx = 0
        t = 0
        max_t = attacker.anim_controller.get_anim_time(act_ani_name)
        hit_idx = 0
        damage_targets = []
        while t < max_t:
            if t >= act_events[idx][1]:
                if act_events[idx][0] == 'mov':
                    attacker.skill_handler.parse_move_node(msg.skill_id, move_node)
                elif act_events[idx][0].startswith('hit'):
                    # 处理一次hit事件
                    hit_idx += 1
                    damage_targets = attacker.skill_handler.handle_attack_hit(msg.skill_id,
                                                                              hit_nodes[act_events[idx][0]],
                                                                              act_events[idx][0], hit_idx, t)
                    if hit_idx >= len(hit_nodes):  # 处理完最后一次，直接退出
                        break
                idx += 1
                if idx >= len(act_events):
                    break
            # 按一帧速度更新
            for player in self.client_id_to_player_map.itervalues():
                if player is None or player.is_dead():
                    continue
                player.move(detect_collision=True)
            t += 33
            if t % 100 == 99:
                t += 1
        for player in self.client_id_to_player_map.itervalues():
            if player is None or player.is_dead():
                continue
            if player not in damage_targets:
                player.recover_movement_state()  # 没被打到的人恢复状态

    def handle_player_defend(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        if player.check_state(conf.STATE_LIEDOWN) or player.check_state(conf.STATE_STIFFNESS):
            # 受击或摔倒的时候不接收移动消息，等客户端玩家受击完之后发送受击完成消息，改变状态才能同步移动消息
            return

        player.sync_position_rotation(msg)

        if conf.DEBUG_SYNC_OPEN:
            self.broadcast(msg)
        else:
            self.broadcast(msg, not_send=player)

    def send_msg_to_player(self, msg, player):
        self.host.sendClient(player.client_hid, msg.marshal())

    def handle_player_hit(self, msg, client_hid):
        """
        客户端动画hit事件触发，计算伤害
        """

        if client_hid not in self.client_id_to_player_map:
            return

        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        # 同步位置
        player.sync_position_rotation(msg)
        # 处理hit
        player.skill_handler.handle_attack_hit(msg.skill_id, msg.node_name)

    def handle_loading_finished(self, msg, client_id):
        from common.events import MsgSCStartGame

        if self.is_game_start is True and self.is_game_stop is False:
            data = MsgSCStartGame().marshal()
            self.host.sendClient(client_id, data)
            # self.send_synchronization_data(client_id) FIX ME !!!!!!!
            return

        self.client_id_finished_map[client_id] = True
        if len(self.client_id_finished_map) >= len(self.client_id_to_player_map):
            data = MsgSCStartGame().marshal()
            for client_id in self.client_id_to_player_map.keys():
                self.host.sendClient(client_id, data)

            self.start_game()

    def handle_player_collect(self, msg, client_hid):
        pass

    def handle_player_reap(self, msg, client_hid):
        # 吃东西
        if msg.entity_id == -1:  # 这里应该根据当前武器来定的，暂时信任客户端,FIX ME !!!
            self.broadcast(msg)
            return
        # 砍树，采浆果等
        entity, model, item = self.universe.get_target_entity(Vector3(msg.pos_x, msg.pos_y, msg.pos_z))
        if item is not None:
            if item.hittable or item.collectible:
                self.broadcast(msg)

    def handle_player_reap_hit(self, msg, client_hid):

        from common.events import MsgSCMapItemDestroy
        from common.events import MsgSCWeaponUninstall

        player = self.client_id_to_player_map[client_hid]

        if msg.entity_id == -1:  # 吃东西
            player.add_health(player.get_attack_value(), msg.blood_percent)
            player.add_spirit(player.get_attack_value(False), msg.power_percent)
            msg_hit = MsgSCPlayerReapHit(player.entity_id, player.health, player.spirit)
            self.broadcast(msg_hit)

            msg_eat = MsgSCSpiritBloodSyn(player.entity_id, player.spirit, player.health)
            self.broadcast(msg_eat)

            # 这里还需要判断食物是否吃完，更换武器
            DebugAux.Log("[server] eat food enter")

            # active_weapon = player.backpack_manager.get_active_weapon()
            # if active_weapon is not None and active_weapon.pile_bool is True:
            # active_weapon.num -= 1
            # die_list = player.backpack_manager.inquire_weapon_die()
            # for id in die_list:
            # msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
            # self.broadcast(msg_tmp)

            # msg_syn = player.backpack_manager.generate_backpack_syn_message_ex()
            # self.send_msg_to_player(msg_syn, player)

            return

        entity, model, item = self.universe.get_target_entity(Vector3(msg.pos_x, msg.pos_y, msg.pos_z))
        if entity and item:
            player = self.client_id_to_player_map[client_hid]
            if item.hittable:
                self.universe.reap(entity, player.get_attack_value(not item.collectible) * msg.attack_percent)

                #DebugAux.Log("reap tree <> ", "player_base_attacck:", player.debug_base_attack(),
                #             " player_weapon_attack:",
                #             player.debug_weapon_attack(), " attack_coefficient:",
                #             msg.attack_percent, " real_damage:", player.get_attack_value(False) * msg.attack_percent)

                # 这里还需要判断食物是否吃完，更换武器
                DebugAux.Log("[server] lop the tree and uninstall weapon if possible")

                # active_weapon = player.backpack_manager.get_active_weapon()
                # if active_weapon is not None:
                # die_list = player.backpack_manager.inquire_weapon_die()
                # for id in die_list:
                # msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
                # self.broadcast(msg_tmp)

                if item.dead:
                    if item.collectible:
                        player.backpack_manager.bring_in_ex(item.good, 1, True)
                        self.send_backpack_syn_message(client_hid)
                    self.universe.destroy(entity)
                    msg = MsgSCMapItemDestroy(entity)
                    self.broadcast(msg)

            elif item.collectible:
                player.backpack_manager.bring_in_ex(item.good, 1, True)
                self.universe.destroy(entity)
                msg = MsgSCMapItemDestroy(entity)
                self.broadcast(msg)
                self.send_backpack_syn_message(client_hid)

    def start_game_count_down(self):
        from common.events import MsgSCStartGame

        if self.is_game_start is True or self.is_game_stop is True:
            return

        if len(self.client_id_finished_map) <= 0:
            self.stop_game()
            return

        DebugAux.Log("[server] arena start_game_count_down... send start game msg")
        data = MsgSCStartGame().marshal()
        for client_id in self.client_id_finished_map.keys():
            self.host.sendClient(client_id, data)

        # remove these delayed clients
        for client_id in self.client_id_to_player_map.keys():
            if self.client_id_finished_map.has_key(client_id) is False:
                self.player_leave(client_id)

        self.start_game()

    # generate the world states and broadcast these states client on the next tick of this arena
    def generate_world_state(self):
        from GameObject.GameObject import GameObject
        from Synchronization.StateSnapshot import State, Snapshot
        sh = Snapshot()
        for entity_id in GameObject.game_object_manager.entity_id_to_gameobject_map.keys():
            if GameObject.game_object_manager.entity_id_to_gameobject_map[entity_id].state_change is True:
                gameobject = GameObject.game_object_manager.entity_id_to_gameobject_map[entity_id]
                state = State(gameobject.entity_id, gameobject.position, gameobject.last_processed_input_num)
                sh.add_state(state)

                # broadcast message .... ??? FIX ME !!!!!!!!!!!!!!!!!!!!!

    def send_backpack_syn_message(self, client_id):
        if self.client_id_to_player_map.has_key(client_id) is False:
            return

        player = self.client_id_to_player_map[client_id]
        msg = player.get_backpack_syn_message()
        DebugAux.Log("[server] " + "send backpack syn message")
        self.host.sendClient(client_id, msg.marshal())

    def handle_make_request(self, client_id, msg):
        if self.client_id_to_player_map.has_key(client_id) is False:
            return

        DebugAux.Log("[server] receive make request msg")
        player = self.client_id_to_player_map[client_id]
        ret = player.backpack_manager.make_request(msg.ID, msg.num)

        if ret is False:
            return

        self.send_backpack_syn_message(client_id)

    def player_drop(self, client_hid, msg):
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return
        player = self.client_id_to_player_map[client_hid]

        drop_item = player.backpack_manager.drop_object_ex(msg.entity_id)
        from common.events import MsgSCMapItemDrop
        self.universe.drop(Vector3().copy(msg), drop_item)
        drop_msg = MsgSCMapItemDrop(msg.x, msg.y, msg.z, drop_item.item)
        self.broadcast(drop_msg)
        # 玩家丢装备到地图上

        self.send_backpack_syn_message(client_hid)

    def weapon_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        DebugAux.Log("[server] weapon install message receive")
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]

        player.backpack_manager.install_weapon_ex(msg.entity_id, msg.slot_index)

        self.send_backpack_syn_message(client_hid)

        item = player.backpack_manager.get_active_weapon()

        if item:
            msg = MsgSCWeaponInstall(msg.pid, item.ID)
            self.broadcast(msg)

    def weapon_uninstall(self, client_hid, msg):
        from common.events import MsgSCWeaponUninstall

        DebugAux.Log("[server] weapon uninstall message receive")

        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.uninstall_weapon_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponUninstall(msg.pid, res.ID)
            self.broadcast(msg)

    def hat_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        DebugAux.Log("[server] hat install message reveive")
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return
        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.install_hat_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponInstall(msg.pid, res.ID)
            self.broadcast(msg)

    def armor_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        DebugAux.Log("[server] armor install message reveive")

        DebugAux.Log("client hid keys : ",self.client_id_to_player_map.keys())
        DebugAux.Log(self.is_game_stop)
        DebugAux.Log(self.username_to_invalid_player_map.keys())

        if client_hid not in self.client_id_to_player_map:
            return
        
        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.install_armor_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponInstall(msg.pid, res.ID)
            self.broadcast(msg)

    def handle_weapon_active(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        from common.events import MsgSCWeaponUninstall

        DebugAux.Log("[server] weapon active message")
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]
        item = player.backpack_manager.active_weapon(msg.entity_id, msg.action)

        if item is not None:
            self.send_backpack_syn_message(client_hid)

        if item is not None:
            if msg.action == 1:
                msg = MsgSCWeaponInstall(msg.pid, item.ID)
                self.broadcast(msg)
            else:
                msg = MsgSCWeaponUninstall(msg.pid, item.ID)
                self.broadcast(msg)

    def gm_backpack_cmd(self, client_hid, msg):
        DebugAux.Log("[server] gm backpack cmd msg received")
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return
        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.gm_add_item(msg.ID, msg.num)
        if res:
            self.send_backpack_syn_message(client_hid)

    def create_bullet(self, msg, client_hid):
        """
        子弹生成
        """
        if client_hid not in self.client_id_to_player_map:
            return

        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        pos = Vector3(msg.px, msg.py, msg.pz)
        direct = Vector3(msg.dx, msg.dy, msg.dz)

        bullet = Bullet(self, pos, direct, player, msg.skill_id, msg.node_name)
        self.bullets[bullet.get_entity_id()] = bullet

        v = bullet.get_move_velocity()
        a = bullet.get_accelerate_velocity()

        # 发送子弹生成消息
        msg = MsgSCBulletSpawn(bullet.get_entity_id(), msg.pid, pos.x, pos.y, pos.z, v.x, v.y, v.z, a.x, a.y, a.z,
                               msg.skill_id, msg.node_name)
        self.broadcast(msg)

    def handle_bullet_hit(self, bullet, hit_target):

        if hit_target is None:
            targets_str = Util.pack_id_pos_health_list_to_string([])
            bullet.owner.get_attack_value()
        else:
            if not hit_target.is_player():
                hit_target.set_player_target(bullet.owner.client_hid)
            hit_target.health_damage(bullet.owner.get_attack_value(), bullet.damage_data.get('percentage'))
            targets_str = Util.pack_id_pos_health_list_to_string(
                [[hit_target.get_entity_id(), hit_target.get_position(), hit_target.get_health()]])

        DebugAux.Log('send hit damage data')
        pos = bullet.get_position()
        msg = MsgSCBulletHit(bullet.get_entity_id(), pos.x, pos.y, pos.z, targets_str)
        self.broadcast(msg)

    def handle_aoe_hit(self, attacker, damage_targets, damage_data, skill_id, node_name, tag, hit_idx):
        """
        处理Aoe攻击
        """
        for target in damage_targets:
            # 扣血
            if not target.is_player():
                target.set_player_target(attacker.client_hid)
            target.health_damage(attacker.get_attack_value(), damage_data.get('percentage'))

            #DebugAux.Log("player: <>", "player_base_attacck:", attacker.debug_base_attack(),
            #             " player_weapon_attack:",
            #             attacker.debug_weapon_attack(), " attack_coefficient:",
            #             damage_data.get("percentage"), " real_damage:",
            #             attacker.get_attack_value(False) * damage_data.get("percentage"))

            # 判断需不需要更新攻击者和受击对象的武器对象 ------------- begin
            from common.events import MsgSCWeaponUninstall

            # 受击打对象武器死亡处理
            # die_list = target.backpack_manager.inquire_weapon_die()

            # msg_syn = target.backpack_manager.generate_backpack_syn_message_ex()
            # self.send_msg_to_player(msg_syn, target)

            # 让其他玩家同步武器挂载卸载数据
            # for id in die_list:
            # msg_syn = MsgSCWeaponUninstall(target.entity_id, id)
            # self.broadcast(msg_syn)

            # 攻击对象武器死亡处理
            # die_list = attacker.backpack_manager.inquire_weapon_die()
            # msg_syn = player.backpack_manager.generate_backpack_syn_message_ex()
            # self.send_msg_to_player(msg_syn, player)

            # 让其他玩家同步武器挂载卸载数据
            # for id in die_list:
            # msg_syn = MsgSCWeaponUninstall(attacker.entity_id, id)
            # self.broadcast(msg_syn)
            # 判断需不需要更新攻击者和受击对象的武器对象 ------------- end

        # self.send_backpack_syn_message(attacker.client_hid)

        targets_str = Util.pack_id_pos_health_list_to_string(
            [x.get_entity_id(), x.get_position(), x.get_health()] for x in damage_targets)

        DebugAux.Log('send hit damage data')
        pos = attacker.get_position()
        rot = attacker.get_rotation()
        msg = MsgSCPlayerHit(attacker.get_entity_id(), pos.x, pos.y, pos.z, rot.x, rot.y, rot.z, skill_id,
                             node_name, tag, hit_idx, targets_str)
        self.broadcast(msg)

    def handle_player_hit_move(self, attacker_pos, targets, node_config, hit_time):

        face = node_config.get('face', True)  # 是否面向攻击者
        move = node_config.get('move')  # 被击速度
        blow_down = node_config.get('blowdown')

        for target in targets:

            move_speed = 0

            if blow_down is not None:  # 进入击倒状态
                if not target.state_machine.can_enter_state(conf.STATE_LIEDOWN):
                    continue
                target.state_machine.change_state(conf.STATE_LIEDOWN)
                move_speed = blow_down
                liedown_time = target.anim_controller.get_anim_time(target.anim_controller.down_anim)
                if target.anim_controller.up_anim is not None:
                    liedown_time += target.anim_controller.get_anim_time(target.anim_controller.up_anim)
                target.set_hit_liedown_start(hit_time + liedown_time)
            else:
                if not target.state_machine.can_enter_state(conf.STATE_STIFFNESS):
                    continue

                # 进入受击状态
                target.state_machine.change_state(conf.STATE_STIFFNESS)
                stiffness_time = target.anim_controller.get_anim_time(node_config.get('hitact'))
                target.set_hit_liedown_start(hit_time + stiffness_time)
                # 设置受击速度
                if move is not None:
                    move_speed = move[0]

            # 直接设置受击者面向和移动速度
            if face:
                target.look_at_position(attacker_pos)

            hit_direct = attacker_pos - target.get_position()
            hit_direct.y = 0
            if not hit_direct.magnitude == 0:
                hit_direct = hit_direct.normalize

            target.set_move_velocity(hit_direct * move_speed)
            target.generate_accelerate_velocity()

    def player_dead(self, player):
        from common.events import MsgSCGameOver
        from common.events import MsgSCMapItemDrop

        msg = MsgSCGameOver()

        self.host.sendClient(player.client_hid, msg.marshal())
        DebugAux.Log("[server] [arena] send game over msg to client")

        drop_items = player.backpack_manager.take_away_all_item()

        for item in drop_items.itervalues():
            self.universe.drop(player.position, item)
            drop_msg = MsgSCMapItemDrop(player.position.x, player.position.y, player.position.z, item.ID)
            self.broadcast(drop_msg)

        DebugAux.Log("[server] [arena] how many player remain ,", len(self.client_id_to_player_map))

    def player_bp_install_uninstall_handler(self, player, die_list):

        for id in die_list:
            msg_syn = MsgSCWeaponUninstall(player.entity_id, id)
            self.broadcast(msg_syn)

        if len(die_list) > 0:
            self.send_backpack_syn_message(player.client_hid)

    def player_bp_weapon_deduce_handler(self, player):
        weapon = player.backpack_manager.get_active_weapon()

        if weapon is not None:
            if weapon.pile_bool is True:
                weapon_blood = weapon.num
            else:
                weapon_blood = weapon.health
        else:
            weapon_blood = -1

        armor = player.backpack_manager.armor
        armor_blood = -1

        if armor is not None:
            armor_blood = armor.health

        hat = player.backpack_manager.hat
        hat_blood = -1

        if hat is not None:
            hat_blood = hat.health

        DebugAux.Log("[server] [arena] ", weapon_blood, " ", armor_blood, " ", hat_blood)
        msg = MsgSCWeaponDeduce(player.entity_id, weapon_blood, armor_blood, hat_blood)
        self.host.sendClient(player.client_hid, msg.marshal())

    def player_spirit_change(self, player):

        if player is None:
            return

        DebugAux.Log("[server] [spirit and blood] syn")
        msg = MsgSCSpiritBloodSyn(player.entity_id, player.spirit, player.health)
        self.broadcast(msg)

    def player_bing_in_handler(self, player, entity_id, ID, health, num):
        from common.events import MsgSCBackpackAdd

        msg = MsgSCBackpackAdd(player.entity_id, entity_id, ID, health, num)
        self.send_msg_to_player(msg, player)

    def player_bp_take_away_handler(self, player, entity_id, ID, health, num):
        from common.events import MsgSCBackpackDel

        msg = MsgSCBackpackDel(player.entity_id, entity_id, ID, health, num)
        self.send_msg_to_player(msg, player)

    def handle_game_win(self):
        msg = MsgSCGameWin()
        self.broadcast(msg)
        self.stop_game()
        DebugAux.Log("[server] [monster manger ] msg win !!!")

    def handle_game_win_count_down(self, remind_time):
        msg = MsgSCGameWinCountDown(remind_time)
        self.broadcast(msg)
        DebugAux.Log("[server] [monster manger ] msg win count down !!!", remind_time)

    def handle_monster_remind(self, waiting_time):
        msg = MsgSCMonsterWaitTime(waiting_time)
        self.broadcast(msg)
        DebugAux.Log("[server] [monster manger ] msg remind time !!!", waiting_time)

    def handle_monster_red_alert(self, alter_time):
        msg = MsgSCMonsterAlertTime(alter_time)
        self.broadcast(msg)
        DebugAux.Log("[server] [monster manger ] msg red alert !!!", alter_time)

    def handle_monster_coming(self, monster_list):
        DebugAux.Log("[server] [monster manger ] msg monster coming !!!", monster_list)
        total_num = 0

        for cell in monster_list:
            total_num += cell.num

        for cell in monster_list:
            for index in xrange(0, cell.num):
                for player in self.client_id_to_player_map.itervalues():
                    info = MonsterDB.get_info_by_ID(cell.ID)
                    born_pos = Util.Vector3(self.universe.get_born_position())

                    monster = Monster(cell.ID, info["health"], born_pos, Util.Vector3(), 999, self)

                    btree = behavior.BehaviorTree()
                    btree.load(AI_Lib.ChaseMonster)
                    monster.set_ai_behavior_tree(btree)
                    monster.set_player_target(player.client_hid)
                    self.group_map[monster.group_id].append(monster)
                    self.entity_id_to_monster_map[monster.entity_id] = monster
                    msg = MsgSCMonsterBorn(monster.entity_id, monster.ID, monster.health, born_pos.x, born_pos.y,
                                           born_pos.z, monster.group_id)
                    self.broadcast(msg)
