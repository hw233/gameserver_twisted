'''
@describe:
          map object
@author:
        sai
@log:
     1. 2017-08-09 created
'''

from GameObject import GameObject


class MapObject(GameObject):
    def __init__(self):
        super(MapObject, self).__init__()
        self.backpack = None
