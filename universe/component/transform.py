from universe.misc import Vector3

class Transform(object):
    def __init__(self, position=None, rotation=None, scale=None, static=True):
        self.position = position if position else Vector3()
        self.rotation = rotation if rotation else Vector3()
        self.scale = scale if scale else Vector3(1.0, 1.0, 1.0)
        self.static = static
