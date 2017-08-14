from common.events import MsgSCPlayerBorn
from GameObject import GameObject

class PlayerBase(object):
    def __init__(self, health, attack, defense, attack_speed, move_speed, make_speed, collect_speed):
        super(PlayerBase, self).__init__()
        self.health = health
        self.attack = attack
        self.defense = defense
        self.attack_speed = attack_speed
        self.move_speed = move_speed
        self.make_speed = make_speed
        self.collect_speed = collect_speed

    def health_damage(self, val):
        '''
        :param val: damage value
        :return: live->true, die->false
        '''
        self.health -= val
        if self.health<=0:
            return False
        else:
            return True


class Player(GameObject, PlayerBase):
    def __init__(self, client_hid, name, position, rotation, player_conf):
        from Configuration.PlayerConf import male
        GameObject.__init__(position, rotation)
        PlayerBase.__init__(male['health'], male['attack'], male['defense'], male['attack_speed'], male['move_speed'], male['make_speed'], male['collect_speed'])
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