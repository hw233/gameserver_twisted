# coding=utf-8

class Navigator(object):
    def __init__(self, destination=None, tolerance=10.0):
        self.destination = destination
        self.speed = None
        self.stopping_distance = None
