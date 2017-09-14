import behavior


class Route(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS