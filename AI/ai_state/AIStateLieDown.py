# coding=utf-8
from common import conf
from state.StateBase import StateBase
import math3d


class StateLieDown(StateBase):
    def __init__(self, name, entity, config):
        super(StateLieDown, self).__init__(name, entity, config)
        self.down_anim = None
        self.up_anim = None
        self.start_up_anim = False

    def enter(self, data):
        self.down_anim = self.get_anim_name()
        self.entity.play_animation(self.down_anim)
        # 两段动作
        self.up_anim = self.get_anim_name('up_ani')
        self.start_up_anim = False

    def execute(self):
        if self.entity.is_anim_at_end():
            if self.up_anim is None or self.start_up_anim:
                self.entity.change_state(conf.STATE_IDLE)
            else:
                self.entity.play_animation(self.up_anim)
                self.start_up_anim = True

    def exit(self):
        self.entity.set_move_velocity(math3d.vector(0, 0, 0))
        self.entity.generate_accelerate_velocity()
        # 需要清空锁帧和震动
        self.entity.frame_stop_count = 0
        self.entity.clear_quake()
