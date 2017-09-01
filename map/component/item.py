# coding=utf-8
class Item(object):
    def __init__(self, id=-1, kind="none", name=None, health=None, reaped=None,
                 drop_good=None, good_id=None):
        self.id = id
        self.kind = kind
        self.name = name
        self.health = health
        self.reaped = reaped
        self.drop_good = drop_good
        self.good_id = good_id

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)

    @property
    def dead(self):
        return self.health <= 0

    @property
    def hittable(self):
        '''
        是否是可被攻击
        :return:
        '''
        return self.kind == 'unit'

    @property
    def collectible(self):
        '''
        是否是可捡起的
        :return:
        '''
        return self.kind == 'good'