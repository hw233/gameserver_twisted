import behavior


class Condition(behavior.BaseNode):
    category = behavior.CONDITION
    
    def __init__(self):
        super(Condition, self).__init__()