'''
   @describe:
'''


class MovementInput(object):
    def __init__(self, direction, delta_time, entity_id, sequence_num):
        self.direction = direction
        self.delta_time = delta_time
        self.entity_id = entity_id
        self.sequence_num = sequence_num