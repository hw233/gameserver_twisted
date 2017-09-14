from .bootstrap import Universe
from .manager import Client, ClientOnly

__all__ = ('Client', 'ClientOnly')

class God(object):
    def __init__(self):
        self._universes = {}

    def remove(self, id):
        if id in self._universes:
            del self._universes

    def get(self, id=0, new=False):
        if new:
            self.remove(id)

        if self._universes.get(id) is None:
            self._universes[id] = Universe()

        return self._universes[id]

_inst = God()
get = _inst.get
remove = _inst.remove
