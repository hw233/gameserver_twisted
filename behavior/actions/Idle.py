import behavior
import time


class Idle(behavior.Action):
    def __init__(self, milliseconds=0):
        super(Idle, self).__init__()
        self.end_time = milliseconds / 1000.

    def open(self, tick):
        start_time = time.time()
        tick.blackboard.set('start_time', start_time, tick.tree.id, self.id)
        tick.tree.host.idle()

    def tick(self, tick):
        curr_time = time.time()
        start_time = tick.blackboard.get('start_time', tick.tree.id, self.id)

        if curr_time - start_time > self.end_time:
            return behavior.SUCCESS

        if tick.tree.host.has_target() is True:
            return behavior.FAILURE

        tick.tree.host.find_nearest_player()

        return behavior.RUNNING

    def set_time(self, interval_time):
        self.end_time = interval_time
