# coding=utf-8
class Item(object):
    def __init__(self, id=-1, kind="none", name=None, health=None, reaped=None,
                 good=None):
        self.id = id
        self.kind = kind
        self.name = name
        self.health = health
        self.reaped = reaped

        # 外部相关
        self.good = good

    def take_damage(self, damage):
        if self.health:
            self.health -= damage
            self.health = max(self.health, 0)

    @property
    def dead(self):
        return self.health <= 0 if self.health is not None else False

    @property
    def hittable(self):
        '''
        是否是可被攻击
        :return:
        '''
        return self.kind == 'fell' or self.kind == 'reap'

    @property
    def collectible(self):
        '''
        是否是可捡起的
        :return:
        '''
        return self.kind == 'good' or self.kind == 'reap'

    @property
    def droppable(self):
        '''
        是否可掉落
        :return:
        '''
        return self.kind == 'fell' and self.good is not None

    @property
    def reapable(self):
        '''
        砍伐后是否有模型
        :return:
        '''
        return self.reaped is not None

    @property
    def none(self):
        return self.kind not in ['good', 'fell', 'reap']
