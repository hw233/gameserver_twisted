'''
    @describe:
              all gameobjects should be managed by this class
    @author:
            sai
    @log:
         1. 2017-08-10 created
'''


class GameObjectManager(object):
    def __init__(self):
        super(GameObjectManager, self).__init__()
        self.entity_id_to_gameobject_map = {}

    def generate_entity_id(self, obj):
        for id in xrange(0, len(self.entity_id_to_gameobject_map) + 1):
            if self.entity_id_to_gameobject_map.has_key(id) is False:
                self.entity_id_to_gameobject_map[id] = obj
                return id

    def get_game_object(self, entity_id):
        if self.entity_id_to_gameobject_map.has_key(entity_id) is False:
            return None
        else:
            return self.entity_id_to_gameobject_map[entity_id]

    def release_game_object(self, entity_id):
        if self.entity_id_to_gameobject_map.has_key(entity_id) is False:
            return
        else:
            del self.entity_id_to_gameobject_map[entity_id]

    def GM_GC(self):
        '''
        server garbage collect, call this function when the server is idle
        :return:
        '''
        import sys

        garbage = []
        for key,val in self.entity_id_to_gameobject_map.items():
            if sys.getrefcount(val) <= 1:
                garbage.append(key)

        for key in garbage:
            del self.entity_id_to_gameobject_map[key]

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
from common.vector import Vector3
from Synchronization.PlayerOperation import OperationManager


class GameObject(object):
    game_object_manager = GameObjectManager()

    def __init__(self,health = 0 , position = Vector3(), rotation = Vector3()):
        # super(GameObject, self).__init__()
        self.position = position
        self.rotation = rotation
        self.health = health
        self.entity_id = GameObject.game_object_manager.generate_entity_id(self)
        self.state_change = False
        self.last_processed_input_num = 0
        self.operation_manager = OperationManager()

        self.backpack_manager = None

    # apply input msg change the rotation and position and so on
    def apply_input(self, move):
        if hasattr(move, 'delta_time') is True and hasattr(move, 'direction') is True\
                and hasattr(move, 'sequence_num'):
            self.position = self.position+move.direction*move.delta_time
            self.last_processed_input_num = move.sequence_num
            self.state_change = True

            # cache the movement
            self.operation_manager.push(move)

    def health_damage(self, val):
        '''
        :param val: damage value
        :return: live->true, die->false
        '''

        if val < 0:
            val = 0

        val = val * (1-self.backpack_manager.get_defense()/100)
        if val < 0:
            val = 0

        self.health -= val

        if self.health <= 0:
            return False
        else:
            return True

    def get_attack_value(self):
        pass







