'''
@describe:
          material object
@author:
        sai
@log:
     1. 2017-08-08 created
'''
from GameObject import GameObject


class BPObjectBase(GameObject):
    def __init__(self, ObjectAttr = None, num = 1):
        super(BPObjectBase, self).__init__()
        if ObjectAttr is None:
            return
        self.ID = ObjectAttr["ID"]
        self.name = ObjectAttr["name"]
        self.icon_num = ObjectAttr["icon_num"]
        self.trade_bool = ObjectAttr["trade_bool"]
        self.pile_bool = ObjectAttr["pile_bool"]
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
        if num <= 0 or num > self.num:
            return

        self.num -= num

        if self.num <= 0:
            GameObject.game_object_manager.release_game_object(self)

    def split(self, num):
        '''
        :param num: partition this object into two diff object, one pile is num, one pile is self.num - num
        :return:
        '''

        obj = type(self)()
        print
        return obj


class KKK(BPObjectBase):
    def __init__(self):
        super(KKK, self).__init__()
        self.some = 10

    def test(self):
        self.split(1)
