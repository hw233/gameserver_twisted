from universe import universe
from universe.component import Transform, Renderer
import math

class TransformProcessor(universe.Processor):
    def __init__(self):
        super(TransformProcessor, self).__init__()

    def start(self, *args, **kwargs):
        pass

    def update(self, dt, *args, **kwargs):
        pass