'''
@describe:
          material object
@author:
        sai
@log:
     1. 2017-08-08 created
     2. 2017-08-15 finish function 'pile' 'consume' 'split'
'''
from GameObject import GameObject


class BPObjectBase(GameObject):
    def __init__(self, object_attr, num=1):
        super(BPObjectBase, self).__init__()
        self.ID = object_attr["ID"]
        self.name = object_attr["name"]
        self.icon_num = object_attr["icon_num"]
        self.trade_bool = object_attr["trade_bool"]
        self.pile_bool = object_attr["pile_bool"]
        self.num = num

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

        # after pile destroy the another material object
        GameObject.game_object_manager.release_game_object(mo)

    def consume(self, num):
        '''
        :param num: deduce the num of this BPObject
        :return: None
        '''
        if num <= 0 or num > self.num:
            return

        self.num -= num

        if self.num <= 0:
            GameObject.game_object_manager.release_game_object(self)

    def split(self, num):
        '''
        :param num: splitting this object to two diff objects, one pile have num objects, one pile have self.num - num objects
        :return: new backpack object has num objects
        '''

        if num > self.num:
            return None

        self.consume(num)

        obj = type(self)()
        entity_id = obj.entity_id
        obj.__dict__ = self.__dict__.copy()
        obj.entity_id = entity_id
        obj.num = num

        return obj
