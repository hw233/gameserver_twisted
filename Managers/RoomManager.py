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


class RoomManager(object):
    SINGLE_ROOM = 0
    NORMAL_ROOM = 1
    BATTLE_ROOM = 2

    def __init__(self, host):
        self.host = host
        self.rid_to_game_room_map = {}
        self.waiting_room = Room(self.generate_room_id(), self.host)
        self.username_to_room_map = {}
        self.client_hid_to_user={}

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
            self.waiting_room = Room(self.generate_room_id(), self.host)

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