# coding=utf-8
import math

from GameObject import GameObject
from common import Util
from common.timer import TimerManager


class Creature(GameObject):
    def __init__(self, health, position, rotation, group_id, arena):
        super(Creature, self).__init__(health, position, rotation)

        self.group_id = group_id
        self.arena = arena

        self.attack = None
        self.defense = None
        self.body_radius = None

        # 移动速度
        self.default_move_speed = None
        self.move_velocity = None

        # 加速度
        self.accelerate_velocity = None

        self.timer_manager = TimerManager()

    def is_move_legal(self):
        pass

    def get_move_velocity(self):
        return self.move_velocity

    def set_move_velocity(self, velocity):
        self.move_velocity = velocity

    def set_accelerate_velocity(self, v):
        self.accelerate_velocity = v

    def get_accelerate_velocity(self):
        return self.accelerate_velocity

    def get_group_id(self):
        return self.group_id

    def get_body_radius(self):
        return self.body_radius

    def in_damage_range(self, other, attack_range):
        """
        判断pos是否在伤害范围内
        扇形攻击范围，需要判断pos离自己的距离以及角度
        """
        v = other.get_position() - self.get_position()
        if v.magnitude > attack_range[0]:
            return False

        angle = Util.vec2_angle(0, 1, v.x, v.z)
        # print '@@@@ ', self.get_rotation().y, ' ', angle, ' --- ', attack_range[1] / 180.0 * math.pi / 2
        angle_diff = self.get_rotation().y - angle
        if abs(angle_diff) > attack_range[1] / 180.0 * math.pi / 2:
            return False
        return True

    def sync_position_rotation(self, msg):
        self.set_position([msg.px, msg.py, msg.pz])
        self.set_rotation([msg.rx, msg.ry, msg.rz])
