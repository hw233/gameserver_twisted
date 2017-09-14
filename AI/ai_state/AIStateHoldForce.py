# coding=utf-8

from common import conf
from state.StateHoldForceBase import StateHoldForceBase


class StateHoldForce(StateHoldForceBase):
    def __init__(self, name, entity, config):
        super(StateHoldForce, self).__init__(name, entity, config)

    def enter(self, data):
        super(StateHoldForce, self).enter(data)
        self.set_anim()

    def execute(self):
        super(StateHoldForce, self).execute()

    def exit(self):
        self.entity.get_state(conf.STATE_IDLE).clear_default_anim()
        self.entity.get_state(conf.STATE_MOVE).clear_default_anim()

        act_name = self.get_act_node_name()
        skill = self.entity.skill_handler.skills[self.sid]
        node_name = skill.config.get(act_name)

        if type(node_name) is list:  # 处理蓄力后的连续动作
            skill.set_start_nodes(node_name)
            self.entity.skill_handler.use_skill(self.sid)
        else:  # 蓄力后只接一个动作
            self.entity.skill_handler.run_skill_node(self.sid, [act_name, ])

        super(StateHoldForce, self).exit()

    def set_anim(self):
        self.entity.get_state(conf.STATE_IDLE).set_default_anim(self.parameters.get('hold_idle'))
        self.entity.get_state(conf.STATE_MOVE).set_default_anim(self.parameters.get('hold_run'))

    def get_speed_percentage(self):
        return self.parameters.get('speed_percentage', 1.0)

    def get_act_node_name(self):
        if self.hold_value >= int(95.0 * self.parameters.get('arrive_percentage')):
            return self.parameters.get('arrive_stage')
        else:
            return self.parameters.get('not_arrive_stage')

    def get_sid(self):
        return self.sid
