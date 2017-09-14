


class StateMachine(object):
    def __init__(self, default, transitions):
        self.state = default
        self.transited = False
        self.transitions = transitions

    def trigger(self, condition):
        transition = self.transitions.get(self.state)
        if transition:
            next_state = transition.get(condition)
            if next_state:
                self.transited = True
                self.state = next_state
