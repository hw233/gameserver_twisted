import behavior


class Composite(behavior.BaseNode):
    category = behavior.COMPOSITE

    def __init__(self, children=None):
        super(Composite, self).__init__()
        self.children = children or []