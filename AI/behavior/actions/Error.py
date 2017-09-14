import AI.behavior


class Error(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.ERROR