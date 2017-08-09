from common import conf
from common.dispatcher import Service


class ArenaServices(Service):
    def __init__(self, host, arena, sid=conf.ARENA_SERVICES):
        super(ArenaServices, self).__init__(sid)
        self.host = host
        self.arena = arena

        commands = {
            0: self.player_move,
            1: self.loading_finished
        }
        self.register_commands(commands)

    def player_move(self, msg, client_hid):
        self.arena.handle_player_move(msg, client_hid)

    def loading_finished(self, msg, client_hid):
        self.arena.handle_loading_finished(msg, client_hid)