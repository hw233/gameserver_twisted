# coding=utf-8
class Renderer(object):
    def __init__(self, gim=None, visible=True, grand_gim=None):
        self.visible = visible
        self.gim = gim
        self.model = None
        self.grand_gim = grand_gim
        self.grand_model = None

class Animator(object):
    def __init__(self, animations):
        self.animations = animations