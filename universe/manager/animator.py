# coding=utf-8
class Transition(object):
    def __init__(self, source, destination, condition):
        self.src = source
        self.dst = destination
        self.cond = condition

class Animator(object):
    def __init__(self, default=None, model=None, transitions=None):
        self.state = default
        self.transitions = transitions
        self.model = model
        if model:
            self.play_animation()

    def bind_model(self, model):
        self.model = model
        self.play_animation()

    def play_animation(self):
        if self.model:
            self.model.play_animation(self.state)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def get_trigger_destination(self, condition):
        for tran in self.transitions:
            if tran.src == self.state and tran.cond == condition:
                return tran.dst

    def trigger(self, condition):
        '''
        触发转移条件
        :param condition: 条件
        :return: 是否转移成功
        '''
        for tran in self.transitions:
            if tran.src == self.state and tran.cond == condition:
                self.state = tran.dst
                self.play_animation()
                return True
        return False