import AI.behavior


class Condition(AI.behavior.BaseNode):
    category = AI.behavior.CONDITION
    
    def __init__(self):
        super(Condition, self).__init__()