'''
    @describe:
              containing all rooms
              1. waiting room
              2. remove invalid room
              3. receive messages and dispatch them to associated rooms
    @author:
             sai
    @log:
         1. 2017-08-02 created
'''


from Managers.GameKindManager import GameKindManager
from common import conf
from common.events import MsgCSGMRoomCmd
from common import EventManager
from common import DebugAux


class RoomManager(object):
    def __init__(self, host):
        self.host = host

        self.game_kind = {}
        self.client_hid_to_game_type = {}
        self.username_to_game_type = {}

        self.msg_dict = {}

        self.init()

    def init(self):
        self.game_kind[GameKindManager.SINGLE_GAME] = GameKindManager(self.host, GameKindManager.SINGLE_GAME)
        self.game_kind[GameKindManager.NORMAL_GAME] = GameKindManager(self.host, GameKindManager.NORMAL_GAME)
        self.game_kind[GameKindManager.BATTLE_GAME] = GameKindManager(self.host, GameKindManager.BATTLE_GAME)

        self.add_msg_listener()

    def add_msg_listener(self):
        EventManager.add_observer(conf.MSG_CS_GM_ROOM_CMD, self.set_room_num)

    def set_room_num(self,client_hid, msg):
        if msg.num <= 0:
            msg.num = 1

        self.game_kind[GameKindManager.NORMAL_GAME].max_room_user_default = msg.num
        self.game_kind[GameKindManager.BATTLE_GAME].max_room_user_default = msg.num
        DebugAux.Log("[server] [room_manager] received gm command set room num ", msg.num)

    def handle_received_msg(self, msg_type, data, client_hid):
        if client_hid not in self.client_hid_to_game_type:
            return

        gkm = self.game_kind[self.client_hid_to_game_type[client_hid]]
        gkm.handle_received_msg(msg_type, data, client_hid)

    def tick(self):
        for game in self.game_kind.itervalues():
            game.tick()

    def add_user(self, user, game_type = -1):
        '''
        :param user:
        :param game_type: if game_type is -1 then there is a reconnect
        :return:
        '''

        if game_type == -1:
            if user in self.username_to_game_type:
                self.game_kind[self.username_to_game_type[user]].add_user()
            return

        self.game_kind[game_type].add_user(user)
        self.username_to_game_type[user.username] = game_type
        self.client_hid_to_game_type[user.client_hid] = game_type

    def remove_user(self, user):
        if user.username not in self.username_to_game_type:
            return

        index = self.username_to_game_type[user.username]

        self.game_kind[index].remove_user(user)

    def is_in_arena(self, user):
        if user.username not in self.username_to_game_type:
            return False

        index = self.username_to_game_type[user.username]
        return self.game_kind[index].is_in_arena(user)
