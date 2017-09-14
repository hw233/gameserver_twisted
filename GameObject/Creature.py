# coding=utf-8
import math
import time

from GameObject import GameObject
from common import Util, conf
from common.timer import TimerManager
from common.vector import Vector3


class Creature(GameObject):
    def __init__(self, health, position, rotation, group_id, arena):
        super(Creature, self).__init__(health, position, rotation)

        self.group_id = group_id
        self.arena = arena

        self.attack = None
        self.defense = None
        self.body_radius = None

        self.timer_manager = TimerManager()

        # state machine
        self.state_machine = None

        # animation controller
        self.anim_controller = None

        # hit recover
        self.hit_start_time = None
        self.hit_time = None

    def update(self):
        # 服务器根据受击或摔倒时间恢复到idle状态
        if self.state_machine.check_cur_state(conf.STATE_STIFFNESS) \
                or self.state_machine.check_cur_state(conf.STATE_LIEDOWN):
            if self.hit_start_time is not None and time.time() - self.hit_start_time >= self.hit_time:
                self.state_machine.change_state(conf.STATE_IDLE)
                self.hit_start_time = None

    def set_hit_liedown_start(self, tim):
        self.hit_start_time = time.time()
        self.hit_time = tim

    def move(self):
        pass

    def is_move_legal(self):
        pass

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
            # print 'too far away: ', v.magnitude
            return False

        angle = Util.vec2_angle(0, 1, v.x, v.z)
        # print '@@@@ ', self.get_rotation().y, ' ', angle, ' --- ', attack_range[1] / 180.0 * math.pi / 2
        angle_diff = self.get_rotation().y - angle
        if abs(angle_diff) > attack_range[1] / 180.0 * math.pi / 2:
            # print 'angle not match: ', angle_diff
            return False
        return True

    def look_at_direction(self, direct):
        angle = Util.vec2_angle(0, 1, direct.x, direct.z)
        self.set_rotation(Vector3(0, angle, 0))

    def look_at_position(self, pos):
        direct = pos - self.get_position()
        self.look_at_direction(direct)

    def sync_position_rotation(self, msg):
        self.set_position([msg.px, msg.py, msg.pz])
        self.set_rotation([msg.rx, msg.ry, msg.rz])

    def generate_accelerate_velocity(self):
        self.accelerate_velocity = Util.generate_friction_accelerate_velocity(self.move_velocity,
                                                                              conf.FRICTION_ACCELERATION)
