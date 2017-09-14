import behavior


class Action(behavior.BaseNode):
    category = behavior.ACTION
    
    def __init__(self):
        super(Action, self).__init__()