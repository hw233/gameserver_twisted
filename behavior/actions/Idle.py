import behavior


class Idle(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS