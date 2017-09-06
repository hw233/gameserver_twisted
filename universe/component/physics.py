# coding=utf-8

from universe.misc import Vector3, AABB

class Collider(object):
    def __init__(self, collider, outline_visible=False):
        self.collider = collider
        self.collisions = []        # 与之碰撞的碰撞器
        self.outline = None
        self.outline_visible = outline_visible
