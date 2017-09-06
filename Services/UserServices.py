from Entity.User import User
from common import conf
from common.dispatcher import Service
from common.events import MsgSCLoginResult
from common import EventManager
import time
import uuid

from common import DebugAux


class GuestUser(object):

    MAX_VALID_TIME = 3600

    def __init__(self):
        super(GuestUser, self).__init__()
        self.username = uuid.uuid4().hex
        self.time_stamp = time.time()


class GuestManager(object):
    def __init__(self):
        super(GuestManager, self).__init__()
        self.guest_info_cache = {}

    def get_guest_acount_info(self, username):

        self.clear_invalid_guest()

        if username not in self.guest_info_cache:
            info = GuestUser()
            self.guest_info_cache[info.username] = info
            return info
        else:
            if time.time()-self.guest_info_cache[username].time_stamp >= GuestUser.MAX_VALID_TIME:
                del self.guest_info_cache[username]
                info = GuestUser()
                self.guest_info_cache[info.username] = info
                return info
            else:
                return self.guest_info_cache[username]

    def clear_invalid_guest(self):
        pass


class UserServices(Service):
    def __init__(self, host, db_manager, room_manager,sid=conf.USER_SERVICES):
        super(UserServices, self).__init__(sid)
        self.host = host

        self.client_hid_to_user_map = {}
        self.username_to_user_map = {}

        self.db_manager = db_manager
        self.room_manager = room_manager
        self.guest_manager = GuestManager()

        commands = {
            0: self.register,
            1: self.login,
            2: self.logout,
            3: self.match_request,
            4: self.match_cancel,
            5: self.client_alive,
        }
        self.register_commands(commands)

        self.init()

    def init(self):
        EventManager.add_observer(conf.MSG_CS_LOGIN_GUEST, self.guest_login)

    def client_alive(self, msg, client_hid):
        pass

    def match_cancel(self, msg, client_hid):
        if self.client_hid_to_user_map.has_key(client_hid) is False:
            return

        DebugAux.Log("matching leave ... ",self.client_hid_to_user_map[client_hid].username)
        self.room_manager.remove_user(self.client_hid_to_user_map[client_hid])

    def match_request(self, msg, client_hid):
        if self.client_hid_to_user_map.has_key(client_hid) is False:
            return

        DebugAux.Log("matching , type ",msg.match_type," username ",self.client_hid_to_user_map[client_hid].username)
        self.room_manager.add_user(self.client_hid_to_user_map[client_hid], msg.match_type)

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

    def guest_login(self, client_hid, msg):
        '''
        :describe: guest login section
        :param client_hid:
        :param msg:
        :return:
        '''
        if self.client_hid_to_user_map.has_key(client_hid) is True:
            return

        guest_info = self.guest_manager.get_guest_acount_info(msg.uuid)
        username = guest_info.username

        DebugAux.Log(username + " is a valid user. login success")
        # valid user
        user = User(self.host, username, client_hid)

        if self.room_manager.is_in_arena(user) is True:
            ''' guest_info.username is the guest username token , user this token to reconnect the server'''
            self.send_login_result(client_hid, guest_info.username, 1)

            '''reconnect'''
            self.room_manager.add_user(user)
        else:
            ''' guest_info.username is the guest username token , user this token to reconnect the server'''
            self.send_login_result(client_hid, guest_info.username, 0)

        self.username_to_user_map[username] = user
        self.client_hid_to_user_map[client_hid] = user

    def login(self, msg, client_hid):
        # same client login again.
        if self.client_hid_to_user_map.has_key(client_hid) is True:
            return

        # authentication
        error_msg, res = self.user_authentication(msg.username, msg.password)
        if error_msg:  # login fail
            self.send_login_result(client_hid, error_msg, -1)
            DebugAux.Log( msg.username+" login failed !")
            return

        username = msg.username

        # diff client same user login again
        if username in self.username_to_user_map:
            # self.logout(None, self.username_to_user_map[username].client_hid)
            self.send_login_result(client_hid, "", 2)
            DebugAux.Log( username + " is already login reject this action")
            return

        DebugAux.Log( username + " is a valid user. login success")
        # valid user
        user = User(self.host, username, client_hid)

        if self.room_manager.is_in_arena(user) is True:
            self.send_login_result(client_hid, '', 1)

            '''reconnect'''
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

        DebugAux.Log( user.username+ " login out")

        self.room_manager.remove_user(user)

        del self.username_to_user_map[self.client_hid_to_user_map[client_hid].username]
        del self.client_hid_to_user_map[client_hid]

    def add_user_to_database(self, username, password):
        return self.db_manager.user_db.add_user_info(username, password)

    def user_authentication(self, username, password):
        return self.db_manager.user_db.user_authentication(username, password)