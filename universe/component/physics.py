# coding=utf-8

class Collider(object):
    def __init__(self, collider, outline_visible=False, static=False):
        self.collider = collider
        self.collisions = []        # 与之碰撞的碰撞器
        self.outline = None
        self.outline_visible = outline_visible
        self.static = static
