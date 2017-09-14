import AI.behavior


class Sequence(AI.behavior.Composite):
    def __init__(self, children = None):
        super(Sequence, self).__init__(children)

    def tick(self, tick):
        for node in self.children:
            status = node._execute(tick)

            if status != AI.behavior.SUCCESS:
                return status

        return AI.behavior.SUCCESS
