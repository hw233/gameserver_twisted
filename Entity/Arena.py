# coding=utf-8
import importlib
import random
from copy import deepcopy

from GameObject.Bullet import Bullet
from common import Util
from common.events import MsgSCPlayerReapHit, MsgSCWeaponUninstall, MsgSCPlayerHit, MsgSCBulletSpawn, MsgSCBulletHit

from common.timer import TimerManager
import universe
from common.vector import Vector3
from common import EventManager
from common import conf
from common import DebugAux
from GameObject.GameObject import GameObject


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

        self.timeManager = TimerManager()

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
        self.group_map = {}  # group_id -> []

    # arena tick
    def tick(self):
        self.timeManager.scheduler()
        dead_bullets = []
        for bid, bullet in self.bullets.iteritems():
            bullet.update()
            if bullet.is_dead():
                dead_bullets.append(bid)
        for bid in dead_bullets:
            del self.bullets[bid]

    def send_map_seed_to_all_clients(self):
        from common.events import MsgSCMapLoad
        import sys
        seed = random.randint(0, sys.maxint)
        msg = MsgSCMapLoad(seed)
        data = msg.marshal()

        for _, user in self.username_to_user.items():
            self.host.sendClient(user.client_hid, data)

        self.universe.start(seed)

    def init_game(self, users):
        from GameObject.Player import Player
        self.username_to_user = users

        # send universe seed to all clients
        self.send_map_seed_to_all_clients()

        for hid, user in self.username_to_user.items():
            if conf.DEBUG_SAME_POSITION:
                born_position = Vector3(-2000, 5, 4000)
            else:
                born_position = Vector3(self.universe.get_born_position())
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

            # add game object event listener [player]
            player.add_listener(GameObject.EVENT_DEAD, self.player_dead)


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

    # def update_arena(self):
    #     pass

    def broadcast(self, msg, not_send=None):
        for player in self.client_id_to_player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def player_quit(self,client_hid, msg):
        from common.events import MsgSCPlayerLeave

        if client_hid not in self.client_id_to_player_map:
            return

        DebugAux.Log("[server] [Arena] receive player quit")

        player = self.client_id_to_player_map[client_hid]

        del self.client_id_to_player_map[client_hid]
        for user in self.username_to_user.itervalues():
            if user.client_hid == client_hid:
                del self.username_to_user[user.username]
                break

        msg = MsgSCPlayerLeave(player.entity_id)
        self.broadcast(msg)

        if len(self.client_id_to_player_map):
            self.stop_game()

    def player_leave(self, client_hid):
        from common.events import MsgSCPlayerLeave
        # player leave the arena
        if self.client_id_to_player_map.has_key(client_hid) is True:
            player = self.client_id_to_player_map[client_hid]
            self.username_to_invalid_player_map[player.name] = player
            del self.client_id_to_player_map[client_hid]
            DebugAux.Log("Server broadcast player leave message")
            msg = MsgSCPlayerLeave(player.entity_id)
            self.broadcast(msg)

        if len(self.client_id_to_player_map) <= 0:
            self.stop_game()

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

        # 需要检测移动的合法性，包括地图边界判断和碰撞检测
        # 之后可以在服务器做的同步策略：
        # 1. 根据客户端服务器时延，利用msg.vx, vy, vz预测服务器速度

        player.sync_position_rotation(msg)

        # broadcast move info to other player
        # self.broadcast(msg, not_send=player) 
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

    def handle_player_attack(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        player.sync_position_rotation(msg)

        DebugAux.Log("player attack")

        # self.broadcast(msg, not_send=player) 
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

        # 武器消耗，并同步
        from common.events import MsgSCWeaponUninstall
        active_weapon = player.backpack_manager.get_active_weapon()
        if active_weapon is not None and active_weapon.pile_bool is True and msg.button_down is False:
            active_weapon.num -= 1
            die_list = player.backpack_manager.inquire_weapon_die()
            for id in die_list:
                msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
                self.broadcast(msg_tmp)

            self.send_backpack_syn_message(client_hid)

    def handle_player_defend(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        player.sync_position_rotation(msg)

        # broadcast move info to other player
        # self.broadcast(msg, not_send=player)
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

    def send_msg_to_player(self, msg, player):
        for hid, obj in self.client_id_to_player_map.items():
            if obj is player:
                self.host.sendClient(hid, msg.marshal())

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
        # from common.events import MsgSCPlayerCollect
        # player = self.client_id_to_player_map[client_hid]
        # print 'handle_player_collect', msg.pid
        # msg = MsgSCPlayerCollect(msg.pid)
        # print 'handle_player_collect22222', client_hid, player.entity_id
        # self.broadcast(msg, player)
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
            player.add_spirit(player.spirit, msg.power_percent)
            msg_hit = MsgSCPlayerReapHit(player.entity_id, player.health, player.spirit)
            self.broadcast(msg_hit)
            # 这里还需要判断食物是否吃完，更换武器
            DebugAux.Log("[server] eat food enter")

            active_weapon = player.backpack_manager.get_active_weapon()
            if active_weapon is not None and active_weapon.pile_bool is True:
                active_weapon.num -= 1
                die_list = player.backpack_manager.inquire_weapon_die()
                for id in die_list:
                    msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
                    self.broadcast(msg_tmp)

            msg_syn = player.backpack_manager.generate_backpack_syn_message_ex()
            self.send_msg_to_player(msg_syn, player)

            return

        entity, model, item = self.universe.get_target_entity(Vector3(msg.pos_x, msg.pos_y, msg.pos_z))
        if entity and item:
            player = self.client_id_to_player_map[client_hid]
            if item.hittable:
                self.universe.reap(entity, player.get_attack_value(not item.collectible) * msg.attack_percent)

                DebugAux.Log("reap tree <> ","player_base_attacck:", player.debug_base_attack(), " player_weapon_attack:",
                             player.debug_weapon_attack(), " attack_coefficient:",
                             msg.attack_percent, " real_damage:", player.get_attack_value(False) * msg.attack_percent)

                # 这里还需要判断食物是否吃完，更换武器
                DebugAux.Log("[server] lop the tree and uninstall weapon if possible")

                active_weapon = player.backpack_manager.get_active_weapon()
                if active_weapon is not None:
                    die_list = player.backpack_manager.inquire_weapon_die()
                    for id in die_list:
                        msg_tmp = MsgSCWeaponUninstall(player.entity_id, id)
                        self.broadcast(msg_tmp)

                if item.dead:
                    self.universe.destroy(entity)
                    msg = MsgSCMapItemDestroy(entity)
                    self.broadcast(msg)
                    if item.collectible:
                        player.backpack_manager.bring_in_ex(item.good)
                        #self.send_backpack_syn_message(client_hid)

            elif item.collectible:
                player.backpack_manager.bring_in_ex(item.good)
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

        # 发送子弹生成消息
        msg = MsgSCBulletSpawn(bullet.get_entity_id(), msg.pid, pos.x, pos.y, pos.z, direct.x, direct.y, direct.z,
                               msg.skill_id, msg.node_name)
        self.broadcast(msg)

    def handle_bullet_destroy(self, bullet, hit_target):

        if hit_target is None:
            targets_str = Util.pack_id_pos_health_list_to_string([])
        else:
            hit_target.health_damage(bullet.owner.get_attack_value(), bullet.damage_data.get('percentage'))
            targets_str = Util.pack_id_pos_health_list_to_string(
                [[hit_target.get_entity_id(), hit_target.get_position(), hit_target.get_health()]])

        DebugAux.Log('send hit damage data')
        pos = bullet.get_position()
        msg = MsgSCBulletHit(bullet.get_entity_id(), pos.x, pos.y, pos.z, targets_str)
        self.broadcast(msg)

    def handle_player_aoe_hit(self, attacker, damage_targets, damage_data, skill_id, node_name):
        """
        处理Aoe攻击
        """
        for target in damage_targets:
            target.health_damage(attacker.get_attack_value(), damage_data.get('percentage'))

            # 判断需不需要更新攻击者和受击对象的武器对象 ------------- begin
            from common.events import MsgSCWeaponUninstall

            # 受击打对象武器死亡处理
            die_list = target.backpack_manager.inquire_weapon_die()

            msg_syn = target.backpack_manager.generate_backpack_syn_message_ex()
            self.send_msg_to_player(msg_syn, target)

            # 让其他玩家同步武器挂载卸载数据
            for id in die_list:
                msg_syn = MsgSCWeaponUninstall(target.entity_id, id)
                self.broadcast(msg_syn)

            # 攻击对象武器死亡处理
            die_list = attacker.backpack_manager.inquire_weapon_die()
            # msg_syn = player.backpack_manager.generate_backpack_syn_message_ex()
            # self.send_msg_to_player(msg_syn, player)

            # 让其他玩家同步武器挂载卸载数据
            for id in die_list:
                msg_syn = MsgSCWeaponUninstall(attacker.entity_id, id)
                self.broadcast(msg_syn)
            # 判断需不需要更新攻击者和受击对象的武器对象 ------------- end

        self.send_backpack_syn_message(attacker.client_hid)

        targets_str = Util.pack_id_pos_health_list_to_string(
            [x.get_entity_id(), x.get_position(), x.get_health()] for x in damage_targets)

        DebugAux.Log('send hit damage data')
        pos = attacker.get_position()
        rot = attacker.get_rotation()
        msg = MsgSCPlayerHit(attacker.get_entity_id(), pos.x, pos.y, pos.z, rot.x, rot.y, rot.z, skill_id, node_name,
                             targets_str)
        self.broadcast(msg)

    def player_dead(self, player):
        from common.events import MsgSCGameOver
        from common.events import MsgSCMapItemDrop

        player = player[0]
        msg = MsgSCGameOver()

        self.host.sendClient(player.client_hid, msg.marshal())
        self.player_quit(player.client_hid, None)
        DebugAux.Log("[server] [arena] send game over msg to client")

        drop_items = player.backpack_manager.take_away_all_item()

        for item in drop_items.itervalues():
            self.universe.drop(player.position, item)
            drop_msg = MsgSCMapItemDrop(player.position.x, player.position.y, player.position.z, item.ID)
            self.broadcast(drop_msg)

        DebugAux.Log("[server] [arena] how many player remain ,",len(self.client_id_to_player_map))
