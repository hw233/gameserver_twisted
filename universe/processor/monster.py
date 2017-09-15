# coding=utf-8
from universe import universe
from universe.component import Monster, Transform, Renderer, Collider, Player
from universe.misc import Vector3

class MonsterProcessor(universe.Processor):
    def __init__(self):
        super(MonsterProcessor, self).__init__()

    def start(self, *args, **kwargs):
        pass

    def update(self, dt, *args, **kwargs):
        pass