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


from Entity.Room import Room
from common import DebugAux


class GameKindManager(object):

    SINGLE_GAME = 0
    NORMAL_GAME = 1
    BATTLE_GAME = 2

    def __init__(self, host, game_type = 0):
        '''
        :param host:
        :param game_type: single 0, normal 1, battle 2
        '''
        self.host = host
        self.game_type = game_type
        self.max_room_user_default = 2
        self.rid_to_game_room_map = {}

        if self.game_type == GameKindManager.SINGLE_GAME:
            self.waiting_room = Room(self.generate_room_id(), self.host, 1)
        else:
            self.waiting_room = Room(self.generate_room_id(), self.host, self.max_room_user_default)

        self.username_to_room_map = {}
        self.client_hid_to_user={}

    def player_quit(self, client_hid, msg):
        if client_hid not in self.client_hid_to_user:
            return

        DebugAux.Log("[server] [GameKindManger] receive player quit")
        user = self.client_hid_to_user[client_hid]
        room = self.username_to_room_map[user.username]
        room.player_quit(client_hid, msg)

        del self.client_hid_to_user[client_hid]
        del self.username_to_room_map[user.username]

    def set_default_room_num(self, num):
        self.max_room_user_default = num
        self.waiting_room.max_user_num = num

    def handle_received_msg(self, msg_type, data, client_hid):
        if self.client_hid_to_user.has_key(client_hid) is False:
            return

        # find room and send msg
        room = self.username_to_room_map[self.client_hid_to_user[client_hid].username]
        room.handle_received_msg(msg_type,data,client_hid)

    def generate_room_id(self):
        for id in xrange(1,len(self.rid_to_game_room_map)+2):
            if self.rid_to_game_room_map.has_key(id) is False:
                return id

    def tick(self):
        invalid_room = []
        for room in self.rid_to_game_room_map.itervalues():
            if room.is_valid() is False:
                invalid_room.append(room)
            else:
                room.tick()

        for room in invalid_room:
            self._remove_room(room)

    def add_user(self, user):
        '''
        :param user:
        :param game_type: if game_type is -1 then there is a reconnect
        :return:
        '''
        # join the room again
        if self.username_to_room_map.has_key(user.username) is True:
            room = self.username_to_room_map[user.username]
            room.add_user(user)
            return

        # new user is coming
        self.waiting_room.add_user(user)
        self.username_to_room_map[user.username] = self.waiting_room
        self.client_hid_to_user[user.client_hid] = user

        if self.waiting_room.is_full() is True:
            self.rid_to_game_room_map[self.waiting_room.rid] = self.waiting_room

            if self.game_type == GameKindManager.SINGLE_GAME:
                self.waiting_room = Room(self.generate_room_id(), self.host, 1)
            else:
                self.waiting_room = Room(self.generate_room_id(), self.host, self.max_room_user_default)

    def remove_user(self, user):
        if self.username_to_room_map.has_key(user.username) is False:
            return

        room = self.username_to_room_map[user.username]

        if room is self.waiting_room:
            room.remove_user(user)
            return

        if room.remove_user(user) is True:
            # The room is empty
            del self.rid_to_game_room_map[room.rid]
            for k,v in room.username_to_user_map.items():
                del self.username_to_room_map[k]

    # remove invalid room
    def _remove_room(self, room):
        del self.rid_to_game_room_map[room.rid]

        for user in room.username_to_user_map.itervalues():
            del self.username_to_room_map[user.username]
            del self.client_hid_to_user[user.client_hid]

    # if the user is already in the arena return True else False
    def is_in_arena(self, user):
        if self.username_to_room_map.has_key(user.username) is True:
            room = self.username_to_room_map[user.username]
            if room is self.waiting_room:
                return False
            else:
                return True

        return False