# coding=utf-8
from common import AnimationEventManager
from state.StateHoldForceBase import StateHoldForceBase


class StateHoldForceSingle(StateHoldForceBase):
    def __init__(self, name, entity, config):
        super(StateHoldForceSingle, self).__init__(name, entity, config)

    def enter(self, data):
        # 暂停攻击动画
        self.entity.pause_animation()
        super(StateHoldForceSingle, self).enter(data)

    def execute(self):
        super(StateHoldForceSingle, self).execute()

    def exit(self):
        # 注册事件
        cur_ani_name = self.entity.get_current_ani_name()
        if self.hold_value >= int(95.0 * self.parameters.get('arrive_percentage')):
            self.register_events(self.parameters.get('arrive_stage'), cur_ani_name)
        else:
            self.register_events(self.parameters.get('not_arrive_stage'), cur_ani_name)
        # 恢复攻击动画
        self.entity.resume_animation()
        # 蓄力条消失
        super(StateHoldForceSingle, self).exit()

    def register_events(self, events, cur_ani_name):
        for tag, args in events.iteritems():
            AnimationEventManager.add(self.entity, cur_ani_name, tag,
                                      self.entity.skill_handler.skills[self.sid].node_map['act'].run_next_nodes, args,
                                      True)
