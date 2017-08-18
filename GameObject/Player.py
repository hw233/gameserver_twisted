from common.events import MsgSCPlayerBorn
from GameObject import GameObject


class PlayerAttributes(object):
    def __init__(self, attack, defense, attack_speed, move_speed, make_speed, collect_speed):
        super(PlayerAttributes, self).__init__()
        self.attack = attack
        self.defense = defense
        self.attack_speed = attack_speed
        self.move_speed = move_speed
        self.make_speed = make_speed
        self.collect_speed = collect_speed


class Player(GameObject, PlayerAttributes):
    def __init__(self, client_hid, name, position, rotation, player_conf):

        from Configuration.PlayerConf import explorer

        GameObject.__init__(self,explorer['health'], position, rotation)
        PlayerAttributes.__init__(self, explorer['attack'], explorer['defense'],
                                  explorer['attack_speed'], explorer['move_speed'], explorer['make_speed'],
                                  explorer['collect_speed'])

        self.client_hid = client_hid
        self.name = name
        self.is_leave_scene = False

        self.speed = player_conf['move_speed']

    def generate_born_msg(self, send_to_others):
        return MsgSCPlayerBorn(self.entity_id, send_to_others, self.name,self.health, self.position[0], self.position[1], self.position[2],self.rotation[0],self.rotation[1], self.rotation[2])

    def set_leave_scene(self):
        self.is_leave_scene = True

    def is_dead(self):
        if self.is_leave_scene:
            return True
        return self.health <= 0

    def update_position(self, pos):
        if self.is_dead():
            return

        self.position[0] = pos[0]
        self.position[1] = pos[1]
        self.position[2] = pos[2]