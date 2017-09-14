import AI.behavior

__all__ = ['Inverter']


class Inverter(AI.behavior.Decorator):
    def tick(self, tick):
        if not self.child:
            return AI.behavior.ERROR

        status = self.child._execute(tick)

        if status == AI.behavior.SUCCESS:
            status = AI.behavior.FAILURE
        elif status == AI.behavior.FAILURE:
            status = AI.behavior.SUCCESS

        return status