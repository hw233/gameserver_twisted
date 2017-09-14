import AI.behavior


class Idle(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.SUCCESS