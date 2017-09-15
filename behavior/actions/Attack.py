import behavior
import time


class Attack(behavior.Action):
    def __init__(self):
        super(Attack, self).__init__()

    def tick(self, tick):

        if tick.tree.host.is_attack_available() is True:
            tick.tree.host.attack_action()
            return behavior.RUNNING

        return behavior.SUCCESS
