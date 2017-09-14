import behavior


class Runner(behavior.Action):
    def tick(self, tick):
        return behavior.RUNNING