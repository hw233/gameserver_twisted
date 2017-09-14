# coding=utf-8
import time

from common import conf
from state.StateBase import StateBase
import math3d


class StateStiffness(StateBase):
    def __init__(self, name, entity, config):
        super(StateStiffness, self).__init__(name, entity, config)

    def enter(self, data):
        anim_name = data.get('anim')
        if anim_name is None:
            return
        anim_time = self.entity.get_ani_time(anim_name)
        hit_time = data.get('hit_time')
        speed = 1.0
        if hit_time is not None and hit_time < anim_time:
            speed = anim_time * 1.0 / hit_time
        self.entity.play_animation(anim_name, speed_rate=speed)

    def execute(self):
        if self.entity.is_anim_at_end():
            self.entity.change_state(conf.STATE_IDLE)

    def exit(self):
        self.entity.set_move_velocity(math3d.vector(0, 0, 0))
        self.entity.generate_accelerate_velocity()
        # 需要清空锁帧和震动
        self.entity.frame_stop_count = 0
        self.entity.clear_quake()
