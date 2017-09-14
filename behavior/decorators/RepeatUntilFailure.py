import behavior


class RepeatUntilFailure(behavior.Decorator):
    def __init__(self, child = None, max_loop=-1):
        super(RepeatUntilFailure, self).__init__(child)

        self.max_loop = max_loop

    def open(self, tick):
        tick.blackboard.set('i', 0, tick.tree.id, self.id)

    def tick(self, tick):
        if not self.child:
            return behavior.ERROR

        i = tick.blackboard.get('i', tick.tree.id, self.id)
        while self.max_loop < 0 or i < self.max_loop:
            status = self.child._execute(tick)

            if status == behavior.SUCCESS:
                i += 1
            else:
                break

        tick.blackboard.set('i', i, tick.tree.id, self.id)
        return status


