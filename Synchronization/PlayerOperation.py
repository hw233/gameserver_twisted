'''
   @describe:
'''

import time


class MovementInput(object):
    def __init__(self, direction, delta_time, entity_id, sequence_num, position):
        self.position = position
        self.direction = direction
        self.delta_time = delta_time
        self.entity_id = entity_id
        self.sequence_num = sequence_num
        self.timestamp = time.time()


class OperationManager(object):
    def __init__(self):
        from collections import deque
        super(OperationManager, self).__init__()
        self.processed_input_cache = deque(maxlen=30)

    def push(self, move):
        self.processed_input_cache.append(move)