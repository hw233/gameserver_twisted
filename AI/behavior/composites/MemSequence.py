import AI.behavior


class MemSequence(AI.behavior.Composite):
    def __init__(self, children=None):
        super(MemSequence, self).__init__(children)

    def open(self, tick):
        tick.blackboard.set('running_child', 0, tick.tree.id, self.id)

    def tick(self, tick):
        idx = tick.blackboard.get('running_child', tick.tree.id, self.id)

        for i in xrange(idx, len(self.children)):
            node = self.children[i]
            status = node._execute(tick)

            if status != AI.behavior.SUCCESS:
                if status == AI.behavior.RUNNING:
                    tick.blackboard.set('running_child', i, tick.tree.id, self.id)
                return status

        return AI.behavior.SUCCESS