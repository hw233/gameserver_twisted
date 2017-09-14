# coding=utf-8

def create_collision_box(box):
    # 显示碰撞格
    c = 0x0000FF00

    edges = [
        ((box.min_point.x, box.min_point.y, box.min_point.z), (box.max_point.x, box.min_point.y, box.min_point.z), c),
        ((box.min_point.x, box.min_point.y, box.min_point.z), (box.min_point.x, box.max_point.y, box.min_point.z), c),
        ((box.min_point.x, box.min_point.y, box.min_point.z), (box.min_point.x, box.min_point.y, box.max_point.z), c),

        ((box.min_point.x, box.max_point.y, box.max_point.z), (box.min_point.x, box.max_point.y, box.min_point.z), c),
        ((box.min_point.x, box.max_point.y, box.max_point.z), (box.min_point.x, box.min_point.y, box.max_point.z), c),
        ((box.min_point.x, box.max_point.y, box.max_point.z), (box.max_point.x, box.max_point.y, box.max_point.z), c),

        ((box.max_point.x, box.min_point.y, box.max_point.z), (box.max_point.x, box.max_point.y, box.max_point.z), c),
        ((box.max_point.x, box.min_point.y, box.max_point.z), (box.min_point.x, box.min_point.y, box.max_point.z), c),
        ((box.max_point.x, box.min_point.y, box.max_point.z), (box.max_point.x, box.min_point.y, box.min_point.z), c),

        ((box.max_point.x, box.max_point.y, box.min_point.z), (box.min_point.x, box.max_point.y, box.min_point.z), c),
        ((box.max_point.x, box.max_point.y, box.min_point.z), (box.max_point.x, box.min_point.y, box.min_point.z), c),
        ((box.max_point.x, box.max_point.y, box.min_point.z), (box.max_point.x, box.max_point.y, box.max_point.z), c),
    ]

    return edges

