class Tick(object):
    def __init__(self, tree = None, target = None, blackboard = None, debug = None):
        self.tree = tree
        self.target = target
        self.blackboard = blackboard
        self.debug = debug

        self._open_nodes = []
        self._node_count = []

    def _enter_node(self, node):
        self._node_count += 1
        self._open_nodes.append(node)

    def _open_node(self, node):
        pass

    def _tick_node(self, node):
        pass

    def _close_node(self, node):
        self._open_nodes.pop()

    def _exit_node(self, node):
        pass
