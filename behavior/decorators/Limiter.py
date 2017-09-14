import behavior

class Limiter(behavior.Decorator):
    def __init__(self,child = None, max_loop = -1):
        super(Limiter, self).__init__(child)
        self.max_loop = max_loop

    def open(self, tick):
        tick.blackboard.set('i', 0, tick.tree.id, self.id)

    def tick(self, tick):
        if not self.child:
            return behavior.ERROR

        i = tick.blackboard.get('i', tick.tree.id, self.id)

        if i < self.max_loop:
            status = self.child._execute(tick)
            if status == behavior.SUCCESS or status == behavior.FAILURE:
                tick.blackboard.set('i', i + 1, tick.tree.id, self.id)

            return status

        return behavior.FAILURE
