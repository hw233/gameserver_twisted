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
            2: self.player_attack,
            3: self.player_hit,
            4: self.player_defend,
            5: self.player_collect,
            8: self.player_reap,
            9: self.player_reap_hit,
            10: self.bullet_spawn,
            11: self.player_position,
            12: self.player_run_act_node,
            13: self.player_hit_recover,
        }
        self.register_commands(commands)

    def player_dress(self, msg, client_id):
        self.arena.handle_player_dress(msg, client_id)

    def player_move(self, msg, client_hid):
        self.arena.handle_player_move(msg, client_hid)

    def player_idle(self, msg, client_hid):
        self.arena.handle_player_idle(msg, client_hid)

    def player_attack(self, msg, client_hid):
        self.arena.handle_player_attack(msg, client_hid)

    def player_hit(self, msg, client_hid):
        self.arena.handle_player_hit(msg, client_hid)

    def player_defend(self, msg, client_hid):
        self.arena.handle_player_defend(msg, client_hid)

    def loading_finished(self, msg, client_hid):
        self.arena.handle_loading_finished(msg, client_hid)

    def player_collect(self, msg, client_hid):
        self.arena.handle_player_collect(msg, client_hid)

    def player_reap(self, msg, client_hid):
        self.arena.handle_player_reap(msg, client_hid)

    def player_reap_hit(self, msg, client_hid):
        self.arena.handle_player_reap_hit(msg, client_hid)

    def bullet_spawn(self, msg, client_hid):
        self.arena.create_bullet(msg, client_hid)

    def player_position(self, msg, client_hid):
        self.arena.handle_player_position(msg, client_hid)

    def player_run_act_node(self, msg, client_hid):
        self.arena.handle_player_run_act_node(msg, client_hid)

    def player_hit_recover(self, msg, client_hid):
        self.arena.handle_player_hit_recover(msg, client_hid)
