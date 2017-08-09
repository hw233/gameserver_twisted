from Entity.User import User
from common import conf
from common.dispatcher import Service
from common.events import MsgSCLoginResult


class UserServices(Service):
    def __init__(self, host, db_manager, room_manager,sid=conf.USER_SERVICES):
        super(UserServices, self).__init__(sid)
        self.host = host

        self.client_hid_to_user_map = {}
        self.username_to_user_map = {}

        self.db_manager = db_manager
        self.room_manager = room_manager

        commands = {
            0: self.register,
            1: self.login,
            2: self.logout,
            3: self.match_request,
            4: self.match_cancel
        }
        self.register_commands(commands)

    def match_cancel(self, msg, client_hid):
        if self.client_hid_to_user_map.has_key(client_hid) is False:
            return
        self.room_manager.remove_user(self.client_hid_to_user_map[client_hid])

    def match_request(self, msg, client_hid):
        if self.client_hid_to_user_map.has_key(client_hid) is False:
            return
        self.room_manager.add_user(self.client_hid_to_user_map[client_hid])

    def send_login_result(self, client_hid, msg, val=0):
        ok = val
        msg_login_result = MsgSCLoginResult(ok, msg)
        self.host.sendClient(client_hid, msg_login_result.marshal())

    def is_user_login(self, client_hid):
        return client_hid in self.client_hid_to_user_map

    def register(self, msg, client_hid):
        if self.add_user_to_database(msg.username, msg.password):
            self.login(msg, client_hid)
        else:
            self.send_login_result(client_hid, "user %s already exist.\n" % msg.username)

    def login(self, msg, client_hid):

        # same client login again.
        if self.client_hid_to_user_map.has_key(client_hid) is True:
            return

        # authentication
        error_msg, res = self.user_authentication(msg.username, msg.password)
        if error_msg:  # login fail
            self.send_login_result(client_hid, error_msg, -1)
            return
        username = msg.username

        # diff client same user login
        if username in self.username_to_user_map:
            # "user login again, kick the old one out"
            self.logout(None, self.username_to_user_map[username].client_hid)

        # valid user
        user = User(self.host, username, client_hid)

        if self.room_manager.is_in_arena(user) is True:
            self.send_login_result(client_hid, '', 1)
            self.room_manager.add_user(user)
        else:
            self.send_login_result(client_hid, '', 0)

        self.username_to_user_map[username] = user
        self.client_hid_to_user_map[client_hid] = user

    def logout(self, msg, client_hid):
        if client_hid not in self.client_hid_to_user_map:
            return
        # Remove it from the room
        user = User(self.host, self.client_hid_to_user_map[client_hid].username, client_hid)
        self.room_manager.remove_user(user)

        del self.username_to_user_map[self.client_hid_to_user_map[client_hid].username]
        del self.client_hid_to_user_map[client_hid]

    def add_user_to_database(self, username, password):
        return self.db_manager.user_db.add_user_info(username, password)

    def user_authentication(self, username, password):
        return self.db_manager.user_db.user_authentication(username, password)
