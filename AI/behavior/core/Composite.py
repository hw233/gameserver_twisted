import AI.behavior


class Composite(AI.behavior.BaseNode):
    category = AI.behavior.COMPOSITE

    def __init__(self, children=None):
        super(Composite, self).__init__()
        self.children = children or []