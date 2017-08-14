# coding=utf-8
import importlib
from copy import deepcopy

from common.timer import TimerManager


class Arena(object):
    def __init__(self, host, arena_conf_filename, player_conf_filename):
        super(Arena, self).__init__()
        self.host = host
        self.client_id_to_player_map = {}
        self.username_to_invalid_player_map = {}
        self.username_to_user = {}

        self.timeManager = TimerManager()

        # arena configuration
        self.arena_conf = importlib.import_module(arena_conf_filename).configuration
        self.player_conf = importlib.import_module(player_conf_filename).configuration

        # game status
        self.is_game_start = False
        self.is_game_stop = False

        # map object [Not Implemented]
        self.map = None
        self.client_id_finished_map={}

    def send_map_seed_to_all_clients(self):
        from common.events import MsgSCMapLoad
        msg = MsgSCMapLoad(-1)   # Not implemented -1 error
        data = msg.marshal()

        for client_id in self.client_id_to_player_map.keys():
            self.host.sendClient(client_id, data)

    def start_game(self):
        self.is_game_start = True
        self.is_game_stop = False

        # update arena/(1000/30ms)
        self.timeManager.add_repeat_timer(1000 / 30, self.update_arena)

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
        # player leave the arena
        if self.client_id_to_player_map.has_key(client_hid) is True:
            player = self.client_id_to_player_map[client_hid]
            self.username_to_invalid_player_map[player.name] = player

        if len(self.client_id_to_player_map)<=0:
            self.stop_game()

    def player_enter_again(self, user):
        from common.events import MsgSCMapLoad

        # user is not in this arena
        if self.username_to_user.has_key(user.username) is False:
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
            msg = player.generate_born_msg(1)  # send to others
            self.broadcast(msg, not_send=player)

    def handle_player_move(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        print "Player Move to:%f %f %f",msg.px,msg.py,msg.pz

        new_pos = [msg.px, msg.py, msg.pz]
        player.update_position(new_pos)

        # broadcast move info to other player
        # self.broadcast(msg, not_send=player) 
        self.broadcast(msg)  # 为了方便调试同步，暂时把角色的移动信息发给他自己，FIX ME !!!!!!!

    def handle_player_idle(self, msg, client_hid):
        if client_hid not in self.client_id_to_player_map:
            return
        player = self.client_id_to_player_map[client_hid]
        if player.is_dead():
            return

        print "Player Idle to:%f %f %f",msg.px,msg.py,msg.pz

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

    def handle_loading_finished(self, msg, client_id):
        from common.events import MsgSCStartGame

        if self.is_game_start is True and self.is_game_stop is False:
            data = MsgSCStartGame().marshal()
            self.host.sendClient(client_id, data)
            self.send_synchronization_data(client_id)
            return

        self.client_id_finished_map[client_id] = True
        if len(self.client_id_finished_map) >= len(self.client_id_to_player_map):
            data = MsgSCStartGame().marshal()
            for client_id in self.client_id_to_player_map.keys():
                self.host.sendClient(client_id, data)

            self.start_game()

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

        # broadcast message .... ???
