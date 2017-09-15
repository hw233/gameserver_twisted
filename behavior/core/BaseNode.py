import uuid
from collections import defaultdict

import behavior
from common import DebugAux


class BaseNode(object):

    category = None

    EVENT_BEGIN = 0
    EVENT_TICK = 1
    EVENT_END = 2

    def __init__(self):
        self.id = str(uuid.uuid1())
        self.title = None
        self.description = ''
        self.parameters = {}
        self.properties = {}

        self.events_listener_map = defaultdict(list)


    @property
    def name(self):
        return self.__class__.__name__

    def _execute(self, tick):
        self._enter(tick)

        if not tick.blackboard.get("is_open", tick.tree.id, self.id):
            self._open(tick)

        status = self._tick(tick)

        if status != behavior.RUNNING:
            self._close(tick)

        self._exit(tick)

        return status

    def _enter(self, tick):
        tick._enter_node(self)
        self.enter(tick)

    def _open(self, tick):
        tick._open_node(self)
        tick.blackboard.set("is_open", True, tick.tree.id, self.id)
        self.open(tick)

    def _tick(self, tick):
        tick._tick_node(self)
        return self.tick(tick)

    def _close(self, tick):
        tick._close_node(self)
        tick.blackboard.set("is_open", False, tick.tree.id, self.id)
        self.close(tick)

    def _exit(self, tick):
        tick._exit_node(self)
        self.exit(tick)

    def enter(self, tick):
        pass

    def open(self, tick):
        pass

    def tick(self, tick):
        pass

    def close(self, tick):
        pass

    def exit(self, tick):
        pass

    def add_listener(self, btype, handler):
        if handler in self.events_listener_map[btype]:
            return
        self.events_listener_map[btype].append(handler)

    def remove_listener(self, btype, handler):
        if handler not in self.events_listener_map[btype]:
            return

        self.events_listener_map[btype].remove(handler)

    def trigger_event(self, btype, *args, **kwargs):
        invalid_list = []
        for fun in self.events_listener_map[btype]:
            try:
                fun(*args, **kwargs)
            except:
                raise
                #invalid_list.append(fun)


        # remove invalid handler in the event list
        for fun in invalid_list:
            self.events_listener_map[btype].remove(fun)

