import behavior


class SearchTarget(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS