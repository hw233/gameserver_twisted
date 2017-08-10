import time


class State(object):
    def __init__(self, entity_id, new_position, last_processed_input = -1):
        super(State, self).__init__()
        self.entity_id = entity_id
        self.new_position = new_position
        self.last_processed_input = last_processed_input


class Snapshot(object):
    snapshot_num = 0

    def __init__(self):
        super(Snapshot, self).__init__()
        self.timestamp = time.time()
        self.snap_num = Snapshot.get_snapshot_num()
        self.states = []

    def add_state(self, state):
        self.states.append(state)

    @staticmethod
    def get_snapshot_num():
        Snapshot.snapshot_num += 1
        return Snapshot.snapshot_num