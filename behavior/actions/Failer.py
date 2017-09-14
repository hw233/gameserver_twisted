import behavior


class Failer(behavior.Action):
    def tick(self, tick):
        return behavior.FAILURE