import AI.behavior
import time


class MaxTime(AI.behavior.Decorator):
    def __init__(self, child, max_time=0):
        super(MaxTime, self).__init__(child)

        self.max_time = max_time

    def open(self, tick):
        t = time.time()
        tick.blackboard.set('startTime', t, tick.tree.id, self.id)

    def tick(self, tick):
        if not self.child:
            return AI.behavior.ERROR

        currTime = time.time()
        startTime = tick.blackboard.get('startTime', tick.tree.id, self.id)

        status = self.child._execute(tick)
        if currTime - startTime > self.max_time:
            return AI.behavior.FAILURE

        return status
