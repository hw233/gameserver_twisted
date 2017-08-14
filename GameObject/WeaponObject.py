'''
@describe:
          material object
@author:
        sai
@log:
     1. 2017-08-08 created
'''
from GameObject import GameObject


class WeaponObject(GameObject):
    def __init__(self, ObjectAttr):
        super(WeaponObject, self).__init__()
        self.ID = ObjectAttr["ID"]
        self.name = ObjectAttr["name"]
        self.icon_num = ObjectAttr["icon_num"]
        self.trade_bool = ObjectAttr["trade_bool"]
        self.pile_bool = ObjectAttr["pile_bool"]










