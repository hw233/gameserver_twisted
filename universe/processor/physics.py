# coding=utf-8
from universe import universe
from universe.component import Transform, Collider
from universe.manager import client, debug

class ColliderProcessor(universe.Processor):
    def __init__(self):
        super(ColliderProcessor, self).__init__()

    def start(self, *args, **kwargs):
        for entity, (tran, coll) in self.world.get_components(Transform, Collider):
            for collider in coll.colliders:
                    # 调试线框
                if coll.outline_visible:
                    if client.get_scene() is not None:
                        prim = client.nexo_world.primitives(client.get_scene())
                        prim.create_line(debug.create_collision_box(collider))
                        coll.outlines.append(prim)

                        prim.position = client.nexo_math3d.vector(
                            tran.position.x,
                            tran.position.y,
                            tran.position.z
                        )

                collider.position = tran.position

    def update(self, dt, *args, **kwargs):
        for entity, (tran, coll) in self.world.get_components(Transform, Collider):
            if coll.static:
                continue

            coll.collisions = []

            for entity_other, (tran_other, coll_other) in self.world.get_components(Transform, Collider):
                if coll != coll_other:
                    for collider in coll.colliders:
                        collider.position = tran.position
                        if collider.intersect(coll_other.colliders):
                            # 碰撞加入碰撞列表
                            coll.collisions.append(coll_other)

            for outline in coll.outlines:
                outline.position = client.nexo_math3d.vector(
                    tran.position.x,
                    tran.position.y,
                    tran.position.z
                )