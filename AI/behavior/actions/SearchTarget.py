import AI.behavior


class SearchTarget(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.SUCCESS