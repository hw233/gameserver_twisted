import behavior


class SearchTarget(behavior.Action):

    def __init__(self):
        super(SearchTarget, self).__init__()

    def open(self, tick):
        pos,val = tick.tree.host.route() # if val is 1 player else 0 route
        node = tick.tree.get_node_by_title("Moving")
        tick.blackboard.set('pox', pos.x, tick.tree.id, node.id)
        tick.blackboard.set('poy', pos.y, tick.tree.id, node.id)
        tick.blackboard.set('poz', pos.z, tick.tree.id, node.id)
        tick.blackboard.set("val", val, tick.tree.id, node.id)

    def tick(self, tick):
        return behavior.SUCCESS