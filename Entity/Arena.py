# coding=utf-8
import importlib
import random
from copy import deepcopy
from common import Util

from common.timer import TimerManager
from Map.MapWorld import MapWorld
from common import EventManager
from common import conf


class Arena(object):
    def __init__(self, host, arena_conf_filename, player_conf_filename):
        super(Arena, self).__init__()

        self.host = host
        self.client_id_to_player_map = {}
        self.username_to_invalid_player_map = {}
        self.username_to_user = {}

        self.timeManager = TimerManager()

        # MapWorld
        self.map_world = MapWorld()

        # arena configuration
        self.arena_conf = importlib.import_module(arena_conf_filename).configuration
        self.player_conf = importlib.import_module(player_conf_filename).explorer

        # game status
        self.is_game_start = False
        self.is_game_stop = False

        # map object [Not Implemented]
        self.client_id_finished_map = {}

    def send_map_seed_to_all_clients(self):
        from common.events import MsgSCMapLoad
        import sys
        seed = random.randint(0, sys.maxint)
        self.map_world.create_world(seed)
        msg = MsgSCMapLoad(seed)

        data = msg.marshal()

        for client_id in self.client_id_to_player_map.keys():
            self.host.sendClient(client_id, data)

    def init_game(self, users):
        from GameObject.Player import Player
        self.username_to_user = users

        # Create player for scene
        born_position = deepcopy(self.arena_conf['player_test_position'])
        born_rotation = deepcopy(self.arena_conf['player_test_rotation'])

        for hid, user in self.username_to_user.items():
            player = Player(user.client_hid, user.username, born_position,
                            born_rotation, self.player_conf)
            self.client_id_to_player_map[user.client_hid] = player

        # send map seed to all clients
        self.send_map_seed_to_all_clients()

        # Send player born message
        self.send_player_born_msg()

        # waiting the clients to load map and resource
        self.timeManager.add_timer(300, self.start_game_count_down)

    def stop_game(self):
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

    def start_game(self):
        self.is_game_start = True
        self.is_game_stop = False

        # update arena/(1000/30ms)
        self.timeManager.add_repeat_timer(1000 / 30, self.update_arena)

        # add various listener
        EventManager.add_observer(conf.MSG_CS_PLAYER_DROP, self.player_drop)
        EventManager.add_observer(conf.MSG_CS_WEAPON_INSTALL, self.weapon_install)
        EventManager.add_observer(conf.MSG_CS_WEAPON_UNINSTALL, self.weapon_uninstall)
        EventManager.add_observer(conf.MSG_CS_ARMOR_INSTALL, self.armor_install)
        EventManager.add_observer(conf.MSG_CS_HAT_INSTALL, self.hat_install)
        EventManager.add_observer(conf.MSG_CS_MAKE_REQUEST, self.handle_make_request)
        EventManager.add_observer(conf.MSG_CS_WEAPON_ACTIVE, self.handle_weapon_active)

    def update_arena(self):
        pass

    # arena tick
    def tick(self):
        self.timeManager.scheduler()

    def broadcast(self, msg, not_send=None):
        for player in self.client_id_to_player_map.itervalues():
            if player is None:
                continue
            if not player == not_send:
                self.host.sendClient(player.client_hid, msg.marshal())

    def player_leave(self, client_hid):
        from common.events import MsgSCPlayerLeave
        # player leave the arena
        if self.client_id_to_player_map.has_key(client_hid) is True:
            player = self.client_id_to_player_map[client_hid]
            self.username_to_invalid_player_map[player.name] = player
            del self.client_id_to_player_map[client_hid]
            print "Server broadcast player leave message"
            msg = MsgSCPlayerLeave(player.entity_id)
            self.broadcast(msg)

        if len(self.client_id_to_player_map) <= 0:
            self.stop_game()

    def player_enter_again(self, user):
        '''
        :param user: user data
        :return: None

        @log:
             1. after some of the map items were destroyed by players.sending map seed to regenerate map is not right.
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

        # notify client to load map
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
        print "send born msg"
        for player in self.client_id_to_player_map.itervalues():
            msg = player.generate_born_msg(0)  # send to itself
            self.host.sendClient(player.client_hid, msg.marshal())
            self.send_backpack_syn_message(player.client_hid)
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

    def handle_player_move(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        # 需要检测移动的合法性，包括地图边界判断和碰撞检测
        # 之后可以在服务器做的同步策略：
        # 1. 根据客户端服务器时延，利用msg.vx, vy, vz预测服务器速度

        new_pos = [msg.px, msg.py, msg.pz]
        player.update_position(new_pos)

        # broadcast move info to other player
        # self.broadcast(msg, not_send=player) 
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

    def handle_player_attack(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        print "Player attack"

        # broadcast move info to other player
        # self.broadcast(msg, not_send=player) 
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

    def send_msg_by_player(self, msg, player):
        for hid, obj in self.client_id_to_player_map.items():
            if obj is player:
                self.host.sendClient(hid, msg.marshal())

    def handle_player_hit(self, msg, client_hid):

        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        # 这里应该需要判定受击是否有效，有效才会向其他客户端发送受击动作，FIX ME !!!!
        hit_data = Util.unpack_string_to_id_pos_list(msg.targets_str)
        for d in hit_data:
            from GameObject.GameObject import GameObject
            target = GameObject.game_object_manager.get_game_object(d[0])
            target.health_damage(player.attack)
            d.append(target.health)

            # 判断需不需要更新攻击者和受击对象的武器对象 ------------- begin
            from common.events import MsgSCWeaponUninstall

            # 受击打对象武器死亡处理
            die_list = target.backpack_manager.inquire_weapon_die()
            if len(die_list) > 0:
                msg = target.backpack_manager.generate_backpack_syn_message_ex()
                self.send_msg_by_player(msg, target)

            # 让其他玩家同步武器挂载卸载数据
            for id in die_list:
                msg = MsgSCWeaponUninstall(target.entity_id, id)
                self.broadcast(msg, target)

            # 攻击对象武器死亡处理
            die_list = player.backpack_manager.inquire_weapon_die()
            if len(die_list) > 0:
                msg = player.backpack_manager.generate_backpack_syn_message_ex()
                self.send_msg_by_player(msg, player)

            # 让其他玩家同步武器挂载卸载数据
            for id in die_list:
                msg = MsgSCWeaponUninstall(player.entity_id, id)
                self.broadcast(msg, player)

                # 判断需不需要更新攻击者和受击对象的武器对象 ------------- end

        print 'send hit damage data'

        msg.targets_str = Util.pack_id_pos_health_list_to_string(hit_data)
        # broadcast move info to other player
        self.broadcast(msg)

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
        from common.events import MsgSCPlayerCollect

        item = self.map_world.get_nearest_item(msg.pos_x, msg.pos_y, msg.pos_z)
        if item:
            print "[server] item id", item.id, item.hittable, item.collectible
            if item.collectible:
                msg = MsgSCPlayerCollect(msg.pid)
                self.broadcast(msg, self.client_id_to_player_map[client_hid])
                print "[server] collect"

                # if this item is a backpack item add this item to the package directly
                # item.data["type"] == "good"
                # Not implemented FIX ME !!!

    def handle_player_reap(self, msg, client_hid):
        from common.events import MsgSCMapItemDestroy
        item = self.map_world.get_nearest_item(msg.pos_x, msg.pos_y, msg.pos_z)
        if item:
            print "[server] item id", item.id, item.hittable, item.collectible
            if item.hittable:
                self.map_world.server_reap(item.id)
                if item.dead:
                    msg = MsgSCMapItemDestroy(item.id)
                    self.broadcast(msg)
                    print "[server] destroy"
                else:
                    print "[server] reap", item.health
                    self.broadcast(msg, self.client_id_to_player_map[client_hid])

    def start_game_count_down(self):
        from common.events import MsgSCStartGame

        if self.is_game_start is True or self.is_game_stop is True:
            return

        if len(self.client_id_finished_map) <= 0:
            self.stop_game()
            return

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
        print "[server] " + "send backpack syn message"
        self.host.sendClient(client_id, msg.marshal())

    def handle_make_request(self, client_id, msg):
        if self.client_id_to_player_map.has_key(client_id) is False:
            return

        print "[server] receive make request msg"
        player = self.client_id_to_player_map[client_id]
        ret = player.backpack_manager.make_request(msg.ID, msg.num)

        if ret is False:
            return

        self.send_backpack_syn_message(client_id)

    def player_drop(self, client_hid, msg):
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return
        player = self.client_id_to_player_map[client_hid]

        player.backpack_manager.drop_object_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

    def weapon_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        print "[server] weapon install message receive"
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]

        player.backpack_manager.install_weapon_ex(msg.entity_id, msg.slot_index)

        self.send_backpack_syn_message(client_hid)

        item = player.backpack_manager.get_active_weapon()

        if item:
            msg = MsgSCWeaponInstall(msg.pid, item.ID)
            self.broadcast(msg, player)

    def weapon_uninstall(self, client_hid, msg):
        from common.events import MsgSCWeaponUninstall

        print "[server] weapon uninstall message receive"

        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.uninstall_weapon_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponUninstall(msg.pid, res.ID)
            self.broadcast(msg, player)

    def hat_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        print "[server] hat install message reveive"
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return
        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.install_hat_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponInstall(msg.pid, res.ID)
            self.broadcast(msg, player)

    def armor_install(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        print "[server] armor install message reveive"

        player = self.client_id_to_player_map[client_hid]
        res = player.backpack_manager.install_armor_ex(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if res:
            msg = MsgSCWeaponInstall(msg.pid, res.ID)
            self.broadcast(msg, player)

    def handle_weapon_active(self, client_hid, msg):
        from common.events import MsgSCWeaponInstall
        print "[server] weapon active message"
        if self.client_id_to_player_map.has_key(client_hid) is False:
            return

        player = self.client_id_to_player_map[client_hid]
        item = player.backpack_manager.active_weapon(msg.entity_id)

        self.send_backpack_syn_message(client_hid)

        if item is not None:
            msg = MsgSCWeaponInstall(msg.pid, item.ID)
            self.broadcast(msg, player)