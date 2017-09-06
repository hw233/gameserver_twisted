
class Processor(object):
    def __init__(self):
        self.world = None

    def update(self, dt, *args):
        raise NotImplementedError