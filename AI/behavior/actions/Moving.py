import AI.behavior


class Moving(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.SUCCESS