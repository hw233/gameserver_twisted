import behavior


class Moving(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS