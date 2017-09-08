# -*- coding: GBK -*-
from Services.UserServices import UserServices
from common import conf
from common import events
from common.dispatcher import Dispatcher
from common.header import Header
from network.simpleHost import SimpleHost
from Database.DBManager import DBManager
from Managers.RoomManager import RoomManager
from common import EventManager
from common import DebugAux


class Server(object):
    def __init__(self, host='', port=2000):
        super(Server, self).__init__()

        # Start host
        self.host = SimpleHost()
        self.host.startup(host, port)

        self.db_manager = DBManager(conf.DB_NAME)
        self.room_manager = RoomManager(self.host)

        self.user_services = UserServices(self.host, self.db_manager, self.room_manager)

        # rooms
        self.rooms = []

        # Generate dispatcher
        self.dispatcher = Dispatcher()
        self.register_dispatcher_services()

        # universe msg_type to message object
        self.msg_dict = None
        self.generate_msg_dict()

        self.user_services_msg_dict = None
        self.room_manager_msg_dict = None

        self.init()

    def init(self):
        self.user_services_msg_dict={
            conf.MSG_CS_LOGIN_GUEST: events.MsgCSLoginGuest(),
        }

        self.room_manager_msg_dict = {
            conf.MSG_CS_GM_ROOM_CMD: events.MsgCSGMRoomCmd(),
            conf.MSG_CS_PLAYER_QUIT: events.MsgCSPlayerQuit(),
        }

    def register_dispatcher_services(self):
        self.dispatcher.register(conf.USER_SERVICES, self.user_services)
        # register MatchServices

    def generate_msg_dict(self):
        self.msg_dict = {
            conf.MSG_CS_REGISTER: events.MsgCSRegister(),
            conf.MSG_CS_LOGIN: events.MsgCSLogin(),
            conf.MSG_CS_LOGOUT: events.MsgCSLogout(),
            conf.MSG_CS_MATCH_REQUEST: events.MsgCSMatchRequest(),
            conf.MSG_CS_MATCH_CANCEL: events.MsgCSMatchCancel(),
            conf.MSG_CS_ALIVE: events.MsgCSAlive(),
        }

    def tick(self):
        # Try send and receive message
        self.host.process()

        # handle received message
        self.handle_received_msg()

        self.room_manager.tick()

    def handle_received_msg(self):
        try:
            # read message from host queue
            event, client_hid, data = self.host.read()

            if event == conf.NET_CONNECTION_DATA:
                # read client data
                msg_type = Header.get_htype_from_raw(data)[0]

                if msg_type in self.msg_dict:
                    msg = self.msg_dict[msg_type]
                    msg.unmarshal(data)
                    # Dispatch message
                    self.dispatcher.dispatch(msg, client_hid)
                elif msg_type in self.user_services_msg_dict:
                    msg = self.user_services_msg_dict[msg_type]
                    msg.unmarshal(data)
                    EventManager.trigger_event(msg_type, client_hid, msg)
                elif msg_type in self.room_manager_msg_dict:
                    msg = self.room_manager_msg_dict[msg_type]
                    msg.unmarshal(data)
                    EventManager.trigger_event(msg_type, client_hid, msg)
                else:
                    # message not register, let room handle it
                    if client_hid in self.user_services.client_hid_to_user_map:
                        self.room_manager.handle_received_msg(msg_type, data, client_hid)
                    else:
                         DebugAux.Log("handle received message error: client not in any room")
            elif event == conf.NET_CONNECTION_LEAVE:
                self.dispatcher.dispatch(self.msg_dict[conf.MSG_CS_LOGOUT], client_hid)
                DebugAux.Log("user connection leave!!!")
            elif event == conf.NET_CONNECTION_NEW:
                DebugAux.Log( "net connection new !!!")
        except:
            raise
            DebugAux.Log( "handle received message error !!!!!!!!")


def main():
    server = Server(conf.SERVER_IP, conf.SERVER_PORT)
    while True:
        server.tick()
        #time.sleep(0.001)


if __name__ == '__main__':
    main()