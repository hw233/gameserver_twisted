
class QuadTree(object):
    def __init__(self, bounds, level=0):
        self.objects = []
        self.nodes = []
        self.level = level
        self.bounds = bounds
        self.MAX_OBJECTS = 10
        self.MAX_LEVELS = 5
