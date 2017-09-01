# coding=utf-8

'''
@describe:
          material object
@author:
        sai
@log:
     1. 2017-08-08 created
     2. 2017-08-15 finish function 'pile' 'consume' 'split'
'''
from Configuration import MaterialDB


class BPItemManager(object):
    def __init__(self):
        super(BPItemManager, self).__init__()
        self.entities_id = []

    def generate_entity_id(self):
        for k in xrange(0, len(self.entities_id)+1):
            if k not in self.entities_id:
                self.entities_id.append(k)
                return k

    def release_entity_id(self, id):
        self.entities_id.remove(id)


bpim = BPItemManager()


class BPItemObject(object):
    def __init__(self, ID, num=1):
        super(BPItemObject, self).__init__()
        self.ID = ID
        self.num = num
        self.pile_bool = True
        self.health = 0
        self.entity_id = bpim.generate_entity_id()

        self.init()

    def init(self):
        self.init_attr()

        if self.pile_bool is False:
            self.num = 1

        self.health = 100

    def init_attr(self):
        info = MaterialDB.get_info_by_ID(self.ID)
        for key, val in info.items():
            setattr(self, key, val)

    def pile(self, mo):
        '''
        :param mo: another material object with same material ID
        :return:
        '''
        if mo.ID != self.ID or mo.num <= 0 or self.pile_bool is False:
            return

        num = mo.num
        mo.consume(num)
        self.num += num

    def consume(self, num):
        '''
        :param num: deduce the num of this BPObject
        :return: None
        '''
        if num <= 0 or num > self.num:
            return

        self.num -= num

    def split(self, num):
        '''
        :param num: splitting this object to two diff objects, one pile have num objects, one pile have self.num - num objects
        :return: new backpack object has num objects
        '''

        if num > self.num or num <= 0:
            return None

        self.consume(num)

        obj = BPItemObject(self.ID, num)

        return obj

    def get_attack(self):
        if hasattr(self, "attack") is True:
            self.health -= self.costblood
            print "[server] backpack item object health ",self.health
            return self.attack
        return 0

    def get_defense(self):
        if hasattr(self, "defense") is True:
            self.health -= self.costblood
            print "[server] backpack item object health ", self.health
            return self.defense

        return 0

    def __del__(self):
        bpim.release_entity_id(self.entity_id)




