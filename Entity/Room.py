from Arena import Arena
from Services.ArenaServices import ArenaServices
from common.dispatcher import Dispatcher
from common.events import *


class Room(object):

    def __init__(self, rid, host, max_user_num=2, arena_conf_filename='Configuration.ArenaConf', player_conf_filename='Configuration.PlayerConf'):
        super(Room, self).__init__()
        self.rid = rid
        self.host = host
        self.arena = None

        self.max_user_num = max_user_num
        self.username_to_user_map = {}

        # Generate dispatcher
        self.dispatcher = Dispatcher()

        # Configuration file
        self.arena_conf_filename = arena_conf_filename
        self.player_conf_filename = player_conf_filename

        # received message
        self.msg_dict = None

    def generate_msg_dict(self):
        self.msg_dict = {
            conf.MSG_CS_PLAYER_MOVE: MsgCSPlayerMove(),
            conf.MSG_CS_PLAYER_ATTACK: MsgCSPlayerAttack(),
            conf.MSG_CS_PLAYER_HIT: MsgCSPlayerHit(),
            conf.MSG_CS_PLAYER_DEFEND: MsgCSPlayerDefend(),
            conf.MSG_CS_LOAD_FINISHED: MsgCSLoadFinished(),
            conf.MSG_CS_PLAYER_COLLECT: MsgCSPlayerCollect(),
            conf.MSG_CS_PLAYER_DROP: MsgCSPlayerDrop(),
            conf.MSG_CS_PLAYER_REAP: MsgCSPlayerReap(),
            conf.MSG_CS_PLAYER_REAP_HIT: MsgCSPlayerReapHit(),
            conf.MSG_CS_MAKE_REQUEST: MsgCSMakeRequest(),
            conf.MSG_CS_WEAPON_INSTALL: MsgCSWeaponInstall(),
            conf.MSG_CS_WEAPON_UNINSTALL: MsgCSWeaponUninstall(),
            conf.MSG_CS_ARMOR_INSTALL: MsgCSArmorInstall(),
            conf.MSG_CS_HAT_INSTALL: MsgCSHatInstall(),
            conf.MSG_CS_WEAPON_ACTIVE: MsgCSWeaponActive(),
            conf.MSG_CS_GM_BP_CMD: MsgCSGMBPCmd(),
        }

    def register_dispatcher_services(self):
        self.dispatcher.register(conf.ARENA_SERVICES, ArenaServices(self.host, self.arena))
        # another services such as combat or trade & not implemented

    def dispatch(self, msg, client_hid):
        self.dispatcher.dispatch(msg, client_hid)

    def handle_received_msg(self, msg_type, data, client_hid):
        from common import EventManager
        if msg_type in self.msg_dict:
            msg = self.msg_dict[msg_type]
            msg.unmarshal(data)
            if hasattr(msg, 'sid'):
                self.dispatcher.dispatch(msg, client_hid)
            else:
                EventManager.trigger_event(msg_type, client_hid, msg)
        else:
            print "Can't handle received message in room"

    def tick(self):
        if self.arena:
            self.arena.tick()

    def start_game(self):
        # Can't start game when game is running
        if self.arena and self.arena.is_game_start and not self.arena.is_game_stop:
            return False

        self.arena = Arena(self.host, self.arena_conf_filename, self.player_conf_filename)

        self.register_dispatcher_services()

        self.generate_msg_dict()

        self.arena.init_game(self.username_to_user_map)

    def add_user(self, user):
        if self.username_to_user_map.has_key(user.username) == False and\
                        len(self.username_to_user_map) >= self.max_user_num:
            return False   # room is full

        # user back again
        if self.arena and not self.arena.is_game_stop:
            self.username_to_user_map[user.username] = user
            self.arena.player_enter_again(user)
            return True

        if self.username_to_user_map.has_key(user.username) is True:
            return

        # new user come
        self.username_to_user_map[user.username] = user
        self.broadcast_roommate_add(user.username)

        if len(self.username_to_user_map) >= self.max_user_num:
            self.start_game()

        return True

    def remove_user(self, user):
        if self.username_to_user_map.has_key(user.username) is False:
            return False   # user not find

        if self.arena and not self.arena.is_game_stop:
            self.arena.player_leave(user.client_hid)
            if self.arena.is_game_stop is True:
                return True
        else:
            del self.username_to_user_map[user.username]
            self.broadcast_roommate_del(user.username)
            if len(self.username_to_user_map) <= 0:
                return True

        return False

    def broadcast_roommate_add(self, username):
        msg = MsgSCRoommateAdd(username)
        data = msg.marshal()

        for username, user in self.username_to_user_map.items():
            self.host.sendClient(user.client_hid, data)

    def broadcast_roommate_del(self, username):
        msg = MsgSCRoommateDel(username)
        data = msg.marshal()

        for username, user in self.username_to_user_map.items():
            self.host.sendClient(user.client_hid, data)

    # game over return True else False
    def is_valid(self):
        if self.arena and not self.arena.is_game_stop:
            return True
        else:
            return False

    def is_full(self):
        if len(self.username_to_user_map) >= self.max_user_num:
            return True
        else:
            return False

