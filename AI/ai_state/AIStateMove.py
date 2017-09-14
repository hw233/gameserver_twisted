# coding=utf-8

from common import AnimationEventManager, SfxManager, conf
from state.StateBase import StateBase

import math3d


class StateMove(StateBase):
    def __init__(self, name, entity, config):
        super(StateMove, self).__init__(name, entity, config)

    def enter(self, data):
        # 设置速度与面向
        self.entity.set_move_velocity(data['velocity'])
        self.entity.set_accelerate_velocity(math3d.vector(0, 0, 0))

        # 包含蓄力子状态
        hold_state = self.entity.get_sub_state(conf.STATE_HOLD_FORCE)
        if hold_state is not None:
            # 这里设置速度变化不能用当前速度，因为网络同步问题，用当前速度有可能会导致速度变化两次
            v = data['velocity']
            v.normalize()
            self.entity.set_move_velocity(v * self.entity.default_move_speed * hold_state.get_speed_percentage())

        defence_state = self.entity.get_sub_state(conf.STATE_DEFENCE)
        if defence_state is not None:
            # 这里设置速度变化不能用当前速度，因为网络同步问题，用当前速度有可能会导致速度变化两次
            v = data['velocity']
            v.normalize()
            self.entity.set_move_velocity(v * self.entity.default_move_speed * defence_state.get_speed_percentage())

        ani_name = self.get_anim_name()
        if not self.entity.is_playing_anim(ani_name):
            self.entity.play_animation(ani_name)
        AnimationEventManager.add(self.entity, ani_name, 'zuo', self.show_foot_print, True)
        AnimationEventManager.add(self.entity, ani_name, 'you', self.show_foot_print, False)

    def execute(self):
        ani_name = self.get_anim_name()
        if not self.entity.is_playing_anim(ani_name):
            self.entity.play_animation(ani_name)

    def show_foot_print(self, is_left_foot):
        pos = self.entity.get_position()
        if is_left_foot:
            sfx = SfxManager.create('fx/other/jiaoyin_zuo.sfx', self.entity.scene_manager.scn)
            sfx.position = math3d.vector(pos.x + 20, pos.y + 10, pos.z)
        else:
            sfx = SfxManager.create('fx/other/jiaoyin_you.sfx', self.entity.scene_manager.scn)
            sfx.position = math3d.vector(pos.x - 20, pos.y + 10, pos.z)

        sfx.rotation_matrix = self.entity.get_rotation()
        sfx.scale = math3d.vector(8, 8, 8)
        sfx.restart()
