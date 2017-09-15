# coding=utf-8
class Renderer(object):
    def __init__(self, gim=None, visible=True, scale=None, animator=None):
        super(Renderer, self).__init__()
        self.visible = visible
        self.gim = gim
        self.model = None
        self.scale = scale
        self.animator = animator

class Shadow(object):
    def __init__(self, gim, visible=True, block=None, position=None, scale=None, animator=None):
        self.gim = gim
        self.visible = visible
        self.block = block
        self.model = position
        self.scale = scale
        self.animator = animator
