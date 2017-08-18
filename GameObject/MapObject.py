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

    def gameobject_born(self, ID, num):
        '''
        :param ID: backpack id
        :param num: object number
        :return: None
        '''
        pass

    def gameobject_destory(self, entity_id):
        '''
        :param entity_id: gameobject entity_id
        :return:
        '''
        pass

    def export_backpack_object(self, entity_id):
        '''
        :param entity_id: backpack object on the ground
        :return: None
        '''
        pass

    def import_backpack_object(self, ID, num, pos):
        '''
        :param ID: backpack object ID
        :param num: backpack object num
        :param pos: location
        :return:
        '''
        pass