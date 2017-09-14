import behavior


class Error(behavior.Action):
    def tick(self, tick):
        return behavior.ERROR