import behavior


class Succeeder(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS