import behavior

__all__ = ['MemPriority']


class MemPriority(behavior.Composite):
    def __init__(self, children=None):
        super(MemPriority, self).__init__(children)

    def open(self, tick):
        tick.blackboard.set('running_child', 0, tick.tree.id, self.id)

    def tick(self, tick):
        idx = tick.blackboard.get('running_child', tick.tree.id, self.id)

        for i in xrange(idx, len(self.children)):
            node = self.children[i]
            status = node._execute(tick)

            if status != behavior.FAILURE:
                if status == behavior.RUNNING:
                    tick.blackboard.set('running_child', i, tick.tree.id, self.id)
                return status

        return behavior.FAILURE