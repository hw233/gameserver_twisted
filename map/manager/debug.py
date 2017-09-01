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

def create_grid_line(grid_width, grid_length, cell_width, cell_length):
    # 绘制网格辅助线
    y = 5
    c = 0xFFFFFFFF
    grid = []
    for column in xrange(0, grid_width + 1):
        x = (column - grid_width / 2) * cell_width
        z = grid_length / 2 * cell_length
        grid.append(((x, y, -z), (x, y, z), c))

    for row in xrange(0, grid_length + 1):
        z = (row - grid_length / 2) * cell_length
        x = grid_width / 2 * cell_width
        grid.append(((-x, y, z), (x, y, z), c))

    return grid

