# coding=utf-8
import time

from state.StateBase import StateBase
from ui import CCUIManager


class StateHoldForceBase(StateBase):
    def __init__(self, name, entity, config):
        super(StateHoldForceBase, self).__init__(name, entity, config)
        self.parameters = None
        self.sid = None
        # 蓄力条参数
        self.hold_start_time = None
        self.hold_bar = None
        self.loop_time = None
        self.hold_value = 0

    def enter(self, data):
        self.parameters = data.get('parameters')
        self.sid = data.get('sid')
        # 蓄力条
        self.hold_start_time = time.time()
        self.loop_time = self.parameters.get('looptime')
        self.hold_value = 0
        # 本地玩家需要显示
        if self.entity.is_local():
            self.hold_bar = CCUIManager.get_ui_by_name('zhandoujiemian.xuli')
            self.hold_bar.show(True)
            self.hold_bar.set_percent(0)

    def execute(self):
        tim = time.time() - self.hold_start_time
        if self.parameters.get('loop') is False:
            if tim >= self.loop_time:
                self.hold_value = 95.0
            else:
                self.hold_value = int(95.0 * tim / self.loop_time)
            pass
        else:
            x = 1.0 * tim / self.loop_time
            res = tim - int(x) * self.loop_time
            self.hold_value = int(95.0 * res / self.loop_time)

        if self.entity.is_local():
            self.hold_bar.set_percent(self.hold_value)

    def exit(self):
        if self.entity.is_local():
            self.hold_bar.show(False)
