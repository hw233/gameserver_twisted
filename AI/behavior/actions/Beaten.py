import AI.behavior


class Beaten(AI.behavior.Action):
    def tick(self, tick):
        return AI.behavior.SUCCESS