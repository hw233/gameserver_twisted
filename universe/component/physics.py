# coding=utf-8

class Collider(object):
    def __init__(self, colliders, outline_visible=False, static=False):
        self.colliders = colliders
        self.collisions = []        # 与之碰撞的碰撞器
        self.outlines = []
        self.outline_visible = outline_visible
        self.static = static

    def intersect(self, other):
        for collider in self.colliders:
            if collider.intersect(other):
                return True
        return False
