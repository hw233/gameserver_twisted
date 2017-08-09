'''
@describe:
          backpack object
          1. tradable object
@author:
        sai
@log:
     1. 2017-08-08 created
'''
from GameObject import GameObject


class BPObject(GameObject):
    def __init__(self, ID = -1, name='', num = 0):
        super(BPObject, self).__init__()
        self.backpack = None
        self.ID = ID
        self.name = name
        self.num = num