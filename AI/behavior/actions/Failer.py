import AI.behavior


class Failer(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.FAILURE