import behavior
from common import DebugAux
from common.vector import Vector3


class Moving(behavior.Action):
    def __init__(self):
        super(Moving, self).__init__()

    def tick(self, tick):
        val = tick.blackboard.get('val', tick.tree.id, self.id)
        x = tick.blackboard.get('pox', tick.tree.id, self.id)
        y = tick.blackboard.get('poy', tick.tree.id, self.id)
        z = tick.blackboard.get('poz', tick.tree.id, self.id)

        target_pos = Vector3(x,y,z)
        pos = tick.tree.host.get_current_position()
        vec = target_pos-pos

        if val == 1: # if val is 1 player else 0 route
            target_pos,val = tick.tree.host.route()

            tick.tree.host.moving(target_pos)

            tick.blackboard.set('val', val, tick.tree.id, self.id)
            tick.blackboard.set('pox', target_pos.x, tick.tree.id, self.id)
            tick.blackboard.set('poy', target_pos.y, tick.tree.id, self.id)
            tick.blackboard.set('poz', target_pos.z, tick.tree.id, self.id)

            vec = target_pos - pos
            distance = vec.magnitude

            if distance < 150:
                return behavior.FAILURE
            elif vec.magnitude > tick.tree.host.unlock_distance:
                tick.tree.host.unlock_player_target()
                return behavior.FAILURE
            else:
                return behavior.RUNNING

        elif val == 0:
            if vec.magnitude < 10:
                return behavior.SUCCESS

            if tick.tree.host.has_target() is True:
                return behavior.FAILURE

            tick.tree.host.moving(target_pos)
        else:
            DebugAux.Log("route error")
            pass

        return behavior.RUNNING