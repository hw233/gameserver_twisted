from .bootstrap import Universe
from .manager import client

__all__ = ('client')

class God(object):
    def __init__(self):
        self._universes = {}

    def get(self, id=0):
        if self._universes.get(id) is None:
            self._universes[id] = Universe()

        return self._universes[id]

_inst = God()
get = _inst.get
