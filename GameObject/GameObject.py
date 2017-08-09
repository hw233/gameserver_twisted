'''
@describe:
          every game entity in the arena should inherit from GameObject
          1. every game entity should have a backpack
          2. every game entity should have a position
          3. every game entity should have an orientation
@author:
        sai
@log:
     1. 2017-08-08 created
'''

entity_id_to_gameobject_map = {}

def generate_entity_id():
    for id in xrange(0, len(entity_id_to_gameobject_map)+1):
        if entity_id_to_gameobject_map.has_key(id) is False:
            return id


def release_entity_id(entity_id):
    if entity_id_to_gameobject_map.has_key(entity_id) is True:
        del entity_id_to_gameobject_map[entity_id]


class GameObject(object):
    def __init__(self, position = [0,0,0], rotation = [0,0,0]):
        super(GameObject, self).__init__()
        self.backpack = {}
        self.position = position
        self.rotation = rotation
        self.entity_id = generate_entity_id()

    def __del__(self):
        release_entity_id(self.entity_id)
