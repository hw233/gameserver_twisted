import behavior


class Decorator(behavior.BaseNode):
    category = behavior.DECORATOR

    def __init__(self, child=None):
        super(Decorator, self).__init__()

        self.child = child or []
