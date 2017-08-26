# -*- coding: utf-8 -*-

from Event import Event


class EventManager(object):
    def __init__(self):
        super(EventManager, self).__init__()
        self.event_map = {}  # { event_type : Event() }

    def add_observer(self, event_type, func, user_data=None):
        event = self.event_map.setdefault(event_type, Event())
        event += (func, user_data)

    def remove_observer(self, event_type, func):
        event = self.event_map.setdefault(event_type, Event())
        event -= func

    def clear_observer(self, event_type):
        event = self.event_map.setdefault(event_type, Event())
        event.clear_observer()

    def trigger_event(self, event_type, *t_args, **d_args):
        event = self.event_map.setdefault(event_type, Event())
        event(*t_args, **d_args)


__event_mgr = EventManager()

# API函数
add_observer = __event_mgr.add_observer

remove_observer = __event_mgr.remove_observer

clear_observer = __event_mgr.clear_observer

trigger_event = __event_mgr.trigger_event
