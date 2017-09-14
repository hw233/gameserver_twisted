# coding=utf-8
from common import conf
from state.StateBase import StateBase
import math3d


class StateAttack(StateBase):
    def __init__(self, name, entity, config):
        super(StateAttack, self).__init__(name, entity, config)

    def enter(self, data):
        self.entity.set_move_velocity(math3d.vector(0, 0, 0))
        self.entity.generate_accelerate_velocity()
        self.entity.skill_handler.set_skill_ready(False)

    def execute(self):
        if self.entity.is_anim_at_end():
            self.entity.change_state(conf.STATE_IDLE)
            self.entity.skill_handler.set_skill_ready(True)

    def exit(self):
        self.entity.set_move_velocity(math3d.vector(0, 0, 0))
        self.entity.generate_accelerate_velocity()
        self.entity.skill_handler.set_skill_ready(True)
