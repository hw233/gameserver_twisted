import behavior


class Beaten(behavior.Action):
    def tick(self, tick):
        return behavior.SUCCESS