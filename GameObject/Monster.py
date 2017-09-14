from Creature import Creature


class Monster(Creature):
    def __init__(self, ID, health, position, rotation, group_id, arena):
        super(Monster, self).__init__(health, position, rotation, group_id, arena)
        self.ID = ID