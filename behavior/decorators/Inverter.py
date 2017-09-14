import behavior

__all__ = ['Inverter']


class Inverter(behavior.Decorator):
    def tick(self, tick):
        if not self.child:
            return behavior.ERROR

        status = self.child._execute(tick)

        if status == behavior.SUCCESS:
            status = behavior.FAILURE
        elif status == behavior.FAILURE:
            status = behavior.SUCCESS

        return status