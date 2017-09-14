# coding=utf-8

from universe.misc import Vector3

class Monster(object):
    def __init__(self, move_speed, attack_speed, attack_range, detection_range):
        self.last_think_time = 0
        self.think_interval = 3

        self.move_speed = move_speed
        self.attack_speed = attack_speed
        self.attack_range = attack_range
        self.detection_range = detection_range

        self.patrol_index = 0
        self.patrol_path = [Vector3(0, 0, 0), Vector3(2000, 0, 2000), Vector3(-2000, 0, 1000)]

        self.target_rotation = Vector3()

        self.last_attack_time = 0

    @property
    def next_patrol_point(self):
        return self.patrol_path[self.patrol_index]

    def move_to_next_point(self):
        self.patrol_index = (self.patrol_index + 1) % len(self.patrol_path)