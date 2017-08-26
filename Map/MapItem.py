# coding=utf-8

from MapGrid import MapBound
from MapMath import Vector3, AABB

class MapItem(object):

    def __init__(self, id, data, position):
        self.id = id
        self.data = data
        self.model = None
        self.health = None
        if 'health' in self.data:
            self.health = self.data['health']

        self.generate_bound(position)
        self.generate_collision()

    def generate_bound(self, position):
        if "width" in self.data and "height" in self.data:
            self.bound = MapBound(
                width=self.data["width"],
                height=self.data["height"],
                position=position
            )
        else:
            self.bound = MapBound()

    def generate_collision(self):
        self.box = None
        # 碰撞盒
        if "collision" in self.data:
            collision = self.data["collision"]
            lbb = Vector3(
                collision["center"]["x"] - collision["box"]["width"] / 2.0,
                collision["center"]["y"] - collision["box"]["height"] / 2.0,
                collision["center"]["z"] - collision["box"]["length"] / 2.0,
            )
            rtf = Vector3(
                collision["center"]["x"] + collision["box"]["width"] / 2.0,
                collision["center"]["y"] + collision["box"]["height"] / 2.0,
                collision["center"]["z"] + collision["box"]["length"] / 2.0,
            )
            self.box = AABB(lbb, rtf)

    @property
    def hittable(self):
        if "type" in self.data:
            return self.data["type"] == 'unit'
        return False

    @property
    def collectible(self):
        if "type" in self.data:
            return self.data["type"] == 'good'
        return False

    @property
    def dead(self):
        if self.health is not None:
            return self.health <= 0
        return False

    def take_damage(self, damage=1):
        if self.health is not None and self.health > 0:
            self.health -= damage
            self.health = max(0, self.health)