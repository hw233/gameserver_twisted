# coding=utf-8
from state.StateBase import StateBase
import math3d


class StateIdle(StateBase):
    def __init__(self, name, entity, config):
        super(StateIdle, self).__init__(name, entity, config)

    def enter(self, data):
        # idle状态直接令速度为0
        self.entity.set_move_velocity(math3d.vector(0, 0, 0))
        self.entity.generate_accelerate_velocity()

    def execute(self):
        if self.entity is None or self.entity.is_dead:
            return

        ani_name = self.get_anim_name()

        if self.entity.is_playing_anim(ani_name):
            return

        if not self.entity.is_playing_any_anim():
            self.entity.play_animation(ani_name)

        # 如果当前动画结束，可以播放静止动画
        if self.entity.is_anim_at_end():
            self.entity.play_animation(ani_name)

        # 如果当前播放的是循环动画，也进行静止动画的播放
        if self.entity.is_playing_loop_anim():
            self.entity.play_animation(ani_name)
