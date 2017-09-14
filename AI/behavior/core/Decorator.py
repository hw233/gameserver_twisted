import AI.behavior


class Decorator(AI.behavior.BaseNode):
    category = AI.behavior.DECORATOR

    def __init__(self, child=None):
        super(Decorator, self).__init__()

        self.child = child or []
