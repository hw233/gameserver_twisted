import behavior


class Sequence(behavior.Composite):
    def __init__(self, children = None):
        super(Sequence, self).__init__(children)

    def tick(self, tick):
        for node in self.children:
            status = node._execute(tick)

            if status != behavior.SUCCESS:
                return status

        return behavior.SUCCESS
