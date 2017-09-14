import AI.behavior


class Action(AI.behavior.BaseNode):
    category = AI.behavior.ACTION
    
    def __init__(self):
        super(Action, self).__init__()