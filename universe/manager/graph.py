# coding=utf-8
import math

NULL = 0
LEFT, RIGHT, TOP, BOTTOM, LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM = range(8)
NEIGHBORS = [LEFT, RIGHT, TOP, BOTTOM]
SIDES = [LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM]
AROUND = NEIGHBORS + SIDES
OFFSET = {
    LEFT: (-1, 0),
    RIGHT: (1, 0),
    TOP: (0, 1),
    BOTTOM: (0, -1),
    LEFT_TOP: (-1, 1),
    RIGHT_TOP: (1, 1),
    LEFT_BOTTOM: (-1, -1),
    RIGHT_BOTTOM: (1, -1)
}
OFFSET_NEIGHBORS = [OFFSET[LEFT], OFFSET[RIGHT], OFFSET[TOP], OFFSET[BOTTOM]]
OFFSET_SIDES = [OFFSET[LEFT_TOP], OFFSET[RIGHT_TOP], OFFSET[LEFT_BOTTOM], OFFSET[RIGHT_BOTTOM]]
OFFSET_AROUND = OFFSET_NEIGHBORS + OFFSET_SIDES

def frange(start, stop, step=1.0):
     x = start
     while x < stop:
        yield x
        x += step

class Boundary(object):
    def __init__(self, left=.0, right=.0, top=.0, bottom=.0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __str__(self):
        return '[l:%d, r:%d, t:%d, b:%d]' % (
            self.left,
            self.right,
            self.top,
            self.bottom,
        )

    def expand(self, horizontal, vertical):
        self.left = min(self.left, horizontal)
        self.right = max(self.right, horizontal)
        self.top = max(self.top, vertical)
        self.bottom = min(self.bottom, vertical)

class Tile(object):
    SIDE_AMOUNT = 4
    def __init__(self, horizontal=0.0, vertical=0.0, lt=NULL, rt=NULL, lb=NULL, rb=NULL):
        '''
        地块
        :param lt: left top
        :param rt: right top
        :param lb: left bottom
        :param rb: right bottom
        '''
        self.horizontal = horizontal
        self.vertical = vertical
        self._corners = {
            LEFT_TOP: lt,
            RIGHT_TOP: rt,
            LEFT_BOTTOM: lb,
            RIGHT_BOTTOM: rb
        }

    def __str__(self):
        return '[h:%f, v:%f, lt:%d, rt:%d, lb:%d, rb:%d]' % (
            self.horizontal,
            self.vertical,
            self._corners[LEFT_TOP],
            self._corners[RIGHT_TOP],
            self._corners[LEFT_BOTTOM],
            self._corners[RIGHT_BOTTOM],
        )

    @property
    def kinds(self):
        return filter(lambda x: x != NULL, sorted(set(self._corners.values())))

    @property
    def filled(self):
        return filter(lambda x: x != NULL, sorted(self._corners.values()))

    @property
    def rank(self):
        counter = {}
        for val in self.filled:
            counter[val] = counter.get(val, 0) + 1
        sorted_counter = sorted(counter.iteritems(), key=lambda x: x[1], reverse=True)
        return map(lambda x: x[0], sorted_counter)

    @property
    def major(self):
        return self.rank[0]

    @property
    def secondary(self):
        return self.rank[1]

    @property
    def partial(self):
        return 4 > self._corners.values().count(NULL) > 0

    @property
    def full(self):
        return self._corners.values().count(NULL) == 0

    @property
    def mixed(self):
        return len(self.kinds) > 1

    def set(self, side, value):
        self._corners[side] = value

    def value(self, key=None):
        if key is None:
            lt = int(self._corners.get(LEFT_TOP, 0) != NULL)
            rt = int(self._corners.get(RIGHT_TOP, 0) != NULL)
            lb = int(self._corners.get(LEFT_BOTTOM, 0) != NULL)
            rb = int(self._corners.get(RIGHT_BOTTOM, 0) != NULL)
        else:
            lt = int(self._corners.get(LEFT_TOP, 0) == key)
            rt = int(self._corners.get(RIGHT_TOP, 0) == key)
            lb = int(self._corners.get(LEFT_BOTTOM, 0) == key)
            rb = int(self._corners.get(RIGHT_BOTTOM, 0) == key)
        return  (rb << 1) | (lb << 0) | (rt << 3) | (lt << 2)

class Node(object):
    def __init__(self, horizontal=0, vertical=0, value=0):
        self.horizontal = horizontal
        self.vertical = vertical
        self.value = value

    def __str__(self):
        return '[h:%d, v:%d]' % (self.horizontal, self.vertical)

    def neighbour(self, direction):
        offset = OFFSET[direction]
        h = self.horizontal + offset[0]
        v = self.vertical + offset[1]
        return Node(horizontal=h, vertical=v)

class Grid(object):
    def __init__(self):
        self.boundary = Boundary()
        self._tiles = {}

    def __str__(self):
        tiles = ''
        pattern = ['?', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                   'J', 'K', 'L', 'M', 'N', 'O', '_', 'Q', 'R', 'S']
        for v in frange(self.boundary.bottom, self.boundary.top + 1):
            for h in frange(self.boundary.left, self.boundary.right + 1):
                tile = self.get_tile(h - 0.5, v - 0.5)
                if tile is None:
                    tiles += ' '
                elif tile.mixed:
                    tiles += '#'
                else:
                    tiles += pattern[tile.value()]
            tiles += '\n'
        return tiles

    def tiles(self, key=None):
        if key is None:
            sorted_tiles = [self._tiles[k] for k in sorted(self._tiles.keys())]
        else:
            sorted_tiles = []
            for k in sorted(self._tiles.keys()):
                if self._tiles[k].major == key:
                    sorted_tiles.append(self._tiles[k])
        return sorted_tiles

    def get_key(self, horizontal, vertical):
        return '%.2f %.2f' % (horizontal, vertical)

    def get_tile(self, horizontal, vertical):
        return self._tiles.get(self.get_key(horizontal, vertical))

    def add_tile(self, tile):
        self.boundary.expand(tile.horizontal, tile.vertical)
        if self.get_tile(tile.horizontal, tile.vertical) is None:
            self._tiles[self.get_key(tile.horizontal, tile.vertical)] = tile

    def remove_tile(self, horizontal, vertical):
        del self._tiles[self.get_key(horizontal, vertical)]

    def validate_chunk(self, min_horizontal, min_vertical,
                       max_horizontal, max_vertical, key=None):
        for h in frange(min_horizontal, max_horizontal + 1):
            for v in frange(min_vertical, max_vertical + 1):
                tile = self.get_tile(h, v)
                if tile is None or not tile.full or tile.mixed:
                    return False
                if key is not None and tile.major != key:
                    return False
        return True

    def remove_chunk(self, min_horizontal, min_vertical,
                       max_horizontal, max_vertical):
        for h in frange(min_horizontal, max_horizontal + 1):
            for v in frange(min_vertical, max_vertical + 1):
                self.remove_tile(h, v)

class Region(object):
    def __init__(self, horizontal_scale=1, vertical_scale=1):
        self.boundary = Boundary()
        self._nodes = {}
        self.horizontal_scale = horizontal_scale
        self.vertical_scale = vertical_scale

    def __str__(self):
        nodes = ''
        pattern = ['!', '@', '#', '$', '%', '^', '&', '*']
        for v in frange(self.boundary.bottom, self.boundary.top + 1):
            for h in frange(self.boundary.left, self.boundary.right + 1):
                node = self.get_node(h, v)
                nodes += pattern[node.value] if node else ' '
            nodes += '\n'
        return nodes

    def local_to_world(self, horizontal, vertical):
        return self.horizontal_scale * horizontal, self.vertical_scale * vertical

    def world_to_local(self, x, z):
        return x / self.horizontal_scale if self.horizontal_scale != 0 else 0, \
               z / self.vertical_scale if self.vertical_scale != 0 else 0

    def grid(self):
        '''
        获取地格数据
        :return:
        '''

        grid = Grid()
        for v in frange(self.boundary.bottom - 1.5, self.boundary.top + 1.5):
            for h in frange(self.boundary.left - 1.5, self.boundary.right + 1.5):
                # 是否已存在
                if grid.get_tile(h, v) is not None:
                    continue

                # 获取四个角节点的值

                lt_node = self.get_node(
                    int(math.floor(h)),
                    int(math.floor(v))
                )
                lt = lt_node.value if lt_node else NULL

                rt_node = self.get_node(
                    int(math.ceil(h)),
                    int(math.floor(v))
                )
                rt = rt_node.value if rt_node else NULL

                lb_node = self.get_node(
                    int(math.floor(h)),
                    int(math.ceil(v))
                )
                lb = lb_node.value if lb_node else NULL

                rb_node = self.get_node(
                    int(math.ceil(h)),
                    int(math.ceil(v))
                )
                rb = rb_node.value if rb_node else NULL

                if lt == rt ==lb == rb == NULL:
                    continue

                # 创建地块
                tile = Tile(horizontal=h, vertical=v,
                            lt=lt, rt=rt, lb=lb, rb=rb)
                grid.add_tile(tile)
        return grid

    def get_node(self, horizontal, vertical):
        return self._nodes.get(self.get_key(horizontal, vertical))

    def get_key(self, horizontal, vertical):
        horizontal = 0.0 if horizontal == -0.0 else horizontal
        vertical = 0.0 if vertical == -0.0 else vertical
        return '%.1f %.1f' % (horizontal, vertical)

    def add_node(self, node):
        '''
        增加节点
        :param node:
        :return:
        '''
        # 扩展边界
        self.boundary.expand(node.horizontal, node.vertical)
        if self.get_node(node.horizontal, node.vertical) is None:
            # 加入节点列表
            self._nodes[self.get_key(node.horizontal, node.vertical)] = node

    def get_nodes(self, value=None):
        if value is not None:
            sorted_nodes = [self._nodes[k] for k in sorted(self._nodes.keys())]
            nodes = filter(lambda x: x.value == value, sorted_nodes)
        else:
            nodes = [self._nodes[k] for k in sorted(self._nodes.keys())]
        return nodes

    @property
    def border_nodes(self):
        nodes = self.get_nodes()
        border = []
        for node in nodes:
            if self.get_node(node.horizontal + 1, node.vertical) is None:
                border.append(node)
                continue
            if self.get_node(node.horizontal, node.vertical + 1) is None:
                border.append(node)
                continue
            if self.get_node(node.horizontal - 1, node.vertical) is None:
                border.append(node)
                continue
            if self.get_node(node.horizontal, node.vertical - 1) is None:
                border.append(node)
                continue
        return border

    def inside(self, horizontal, vertical, padding=0, key=None):
        '''
        判断点是否在区域内部
        :param horizontal:
        :param vertical:
        :param padding: 边缘间隔
        '''
        for h in frange(horizontal - padding, horizontal + padding + 1):
            for v in frange(vertical - padding, vertical + padding + 1):
                node = self.get_node(h, v)
                if not node:
                    return False
                if key is not None and node.value != key:
                    return False
        return True

    def validate_boundary(self, boundary):
        '''
        检查区域
        :param boundary:
        :return: 区域内所有位置是否都有节点
        '''
        for v in frange(boundary.bottom, boundary.top + 1):
            for h in frange(boundary.left, boundary.right + 1):
                node = self.get_node(h, v)
                if node is None:
                    return False
        return True