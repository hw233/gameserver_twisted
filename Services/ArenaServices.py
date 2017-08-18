from common import conf
from common.dispatcher import Service


class ArenaServices(Service):
    def __init__(self, host, arena, sid=conf.ARENA_SERVICES):
        super(ArenaServices, self).__init__(sid)
        self.host = host
        self.arena = arena

        commands = {
            0: self.loading_finished,
            1: self.player_move,
            2: self.player_idle,
            3: self.player_attack,
            4: self.player_hit,
            5: self.player_collect,
            6: self.player_drop,
        }
        self.register_commands(commands)

    def player_move(self, msg, client_hid):
        self.arena.handle_player_move(msg, client_hid)

    def player_idle(self, msg, client_hid):
        self.arena.handle_player_idle(msg, client_hid)

    def player_attack(self, msg, client_hid):
        self.arena.handle_player_attack(msg, client_hid)

    def player_hit(self, msg, client_hid):
        self.arena.handle_player_hit(msg, client_hid)

    def loading_finished(self, msg, client_hid):
        self.arena.handle_loading_finished(msg, client_hid)

    def player_collect(self, msg, client_hid):
        self.arena.handle_player_collect(msg, client_hid)

    def player_drop(self, msg, client_hid):
        self.arena.handle_player_drop(client_hid, msg)