# coding=utf-8
from universe import universe
from universe.component import Transform, Collider
from universe.manager import client, debug

class ColliderProcessor(universe.Processor):
    def __init__(self):
        super(ColliderProcessor, self).__init__()

    def start(self, *args, **kwargs):
        for entity, (tran, coll) in self.world.get_components(Transform, Collider):
            # 调试线框
            if coll.outline_visible:
                if client.get_scene() is None:
                    return
                prim = client.nexo_world.primitives(client.get_scene())
                prim.create_line(debug.create_collision_box(coll.collider))
                coll.outline = prim

                prim.position = client.nexo_math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )
            coll.collider.position = tran.position

    def update(self, dt, *args, **kwargs):
        for entity, (tran, coll) in self.world.get_components(Transform, Collider):
            if coll.static:
                continue
            if coll.outline_visible:
                coll.outline.position = client.nexo_math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )
            coll.collisions = []
            coll.collider.position = tran.position
            for entity_other, (tran_other, coll_other) in self.world.get_components(Transform, Collider):
                if coll != coll_other:
                    if coll.collider.intersect(coll_other.collider):
                        # 碰撞加入碰撞列表
                        coll.collisions.append(coll_other)
