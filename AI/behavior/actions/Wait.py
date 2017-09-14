import AI.behavior
import time


class Wait(AI.behavior.Action):
    def __init__(self, milliseconds=0):
        super(Wait, self).__init__()
        self.end_time = milliseconds/1000.

    def open(self, tick):
        start_time = time.time()
        tick.blackboard.set('start_time', start_time, tick.tree.id, self.id)

    def tick(self, tick):
        curr_time = time.time()
        start_time = tick.blackboard.get('start_time', tick.tree.id, self.id)

        if curr_time-start_time > self.end_time:
            return AI.behavior.SUCCESS

        return AI.behavior.RUNNING