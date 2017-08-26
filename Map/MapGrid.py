# coding=utf-8

from MapMath import GridPosition
import math


class MapBound(object):
    '''
    边界
    '''
    def __init__(self, width=0, height=0, position=None):
        self._width = width
        self._height = height

        if position is None:
            self._position = GridPosition(0, 0)
        else:
            self._position = position

        self.calculate_border()

    def __str__(self):
        return 'w=%f, h=%f, c=(%f, %f), l=%f, r=%f, t=%f, b=%f' % \
               (self._width, self._height, self._position.row, self._position.column,
                self.left, self.right, self.top, self.bottom)

    def calculate_border(self):
        '''
        重新计算边界
        :return:
        '''
        self._left = self.position.column - self.width / 2.0
        self._right = self.position.column + self.width / 2.0
        self._top = self.position.row - self.height / 2.0
        self._bottom = self.position.row + self.height / 2.0

    def calculate_size(self):
        '''
        重新计算中心点和宽度
        :return:
        '''
        self.position.column = (self.left + self.right) / 2.0
        self.position.row = (self.bottom + self.top) / 2.0
        self._width = self.right - self.left + 1.0
        self._height = self.bottom - self.top + 1.0

    def extend(self, position):
        '''
        扩展区域
        :param position: 需要包括的点位置
        :return:
        '''
        self._left = min(self._left, position.column)
        self._right = max(self._right, position.column + 1)
        self._top = min(self._top, position.row)
        self._bottom = max(self._bottom, position.row + 1)
        self.calculate_size()

    # def is_inside(self, position):
    #     '''
    #     某点是否位于物件矩形范围内
    #     :param position: 网格坐标
    #     :return:
    #     '''
    #     delta = position - self.position
    #     if -self.data["width"] / 2 <= delta.column <= self.data["width"] / 2:
    #         if -self.data["height"] / 2 <= delta.row <= self.data["height"] / 2:
    #             return True
    #     return False

    def distance_to(self, other):
        delta = self.position - other.position
        return math.sqrt(delta.row ** 2 + delta.column ** 2)

    def intersect(self, other):
        '''
        两个区域是否相交
        :param other:
        :return:
        '''
        r1, c1 = self.position.row, self.position.column
        r2, c2 = other.position.row, other.position.column
        if math.fabs(c1 - c2) * 2 > self.width + other.width:
            return False
        if math.fabs(r1 - r2) * 2 > self.height + other.height:
            return False
        return True

    @property
    def all(self):
        '''
        遍历区域内坐标迭代器
        :return:
        '''
        for row in xrange(int(round(self.top)), int(round(self.bottom + 1))):
            for column in xrange(int(round(self.left)), int(round(self.right + 1))):
                yield GridPosition(row, column)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = GridPosition(value.row, value.column)
        self.calculate_border()

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Grid(object):
    '''
    网格
    '''
    LEFT, RIGHT, TOP, BOTTOM, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT = range(8)
    STRAIGHT_NEIGHBORS_OFFSET = [
        GridPosition( 0, -1),     # LEFT
        GridPosition( 0,  1),     # RIGHT
        GridPosition(-1,  0),     # TOP
        GridPosition( 1,  0),     # BOTTOM
    ]
    LEAN_NEIGHBORS_OFFSET = [
        GridPosition(-1, -1),     # TOP_LEFT
        GridPosition(-1,  1),     # TOP_RIGHT
        GridPosition( 1, -1),     # BOTTOM_LEFT
        GridPosition( 1,  1),     # BOTTOM_RIGHT
    ]
    NEIGHBORS_OFFSET = STRAIGHT_NEIGHBORS_OFFSET + LEAN_NEIGHBORS_OFFSET

    def __init__(self, width, height, cell_width, cell_height):
        self._bound = MapBound(width, height, GridPosition(width / 2, height / 2))
        self._cell_bound = MapBound(cell_width, cell_height)
        self.grid_map = []
        for row in xrange(self.bound.height):
            self.grid_map.append([])
            for column in xrange(self.bound.width):
                cell = Cell(GridPosition(row, column))
                self.grid_map[-1].append(cell)

        self.block_manager = None

    def __str__(self):
        '''
        打印网格
        :return:
        '''
        ret = []
        for row in xrange(len(self.grid_map)):
            ret.append(''.join([cell for cell in self.grid_map[row]]))
        return '\n'.join(ret)

    def set_block_manager(self, block_manager):
        self.block_manager = block_manager

    @property
    def bound(self):
        return self._bound

    @property
    def cell_bound(self):
        return self._cell_bound

    def get_cell(self, position):
        if 0 <= position.row < self.bound.height:
            if 0 <= position.column < self.bound.width:
                row = int(round(position.row))
                column = int(round(position.column))
                return self.grid_map[row][column]

    def get_cell_neighbor(self, cell, direction):
        offset = self.NEIGHBORS_OFFSET[direction]
        if isinstance(cell, GridPosition):
            return self.get_cell(cell + offset)
        elif isinstance(cell, Cell):
            return self.get_cell(cell.position + offset)

    def fill_cells(self, top_left_position, value):
        '''
        填充2*2网格
        :param top_left_position: 处于左上角的网格坐标
        :param value: 填充的值
        :return: 新填充的比例
        '''
        # A A B B
        #  -----
        # A|A B|B
        # C|C D|D
        #  -----
        # C C D D
        # 填充中间的A B C D的四个角
        count = 0.0
        # 左上
        cell = self.get_cell(top_left_position)
        if cell:
            is_new = cell.fill_corner(Corner.BOTTOM_RIGHT, value)
            count += 0.25 if is_new else 0.0

        # 右上
        cell = self.get_cell_neighbor(top_left_position, self.RIGHT)
        if cell:
            is_new = cell.fill_corner(Corner.BOTTOM_LEFT, value)
            count += 0.25 if is_new else 0.0

        # 左下
        cell = self.get_cell_neighbor(top_left_position, self.BOTTOM)
        if cell:
            is_new = cell.fill_corner(Corner.TOP_RIGHT, value)
            count += 0.25 if is_new else 0.0

        # 右下
        cell = self.get_cell_neighbor(top_left_position, self.BOTTOM_RIGHT)
        if cell:
            is_new = cell.fill_corner(Corner.TOP_LEFT, value)
            count += 0.25 if is_new else 0.0

        return count

    def clear_cells(self, top_left_position):
        self.fill_cells(top_left_position, Corner.CORNER_NULL)

    def vector_to_grid(self, x, z):
        '''
        浮点向量转网格坐标
        :param x:
        :param z:
        :return:
        '''
        column = x / self._cell_bound.width
        row = z / self._cell_bound.height
        pos = GridPosition(row, column).absolute_by(self.bound.position)
        return pos

    def grid_to_vector(self, position):
        relate_pos = position.relate_to(self.bound.position)
        x = relate_pos.column * self._cell_bound.width
        z = relate_pos.row * self._cell_bound.height
        return x, z


class Corner(object):
    CORNER_NULL = 0
    MAX_CORNER_AMOUNT = 4
    TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT = range(MAX_CORNER_AMOUNT)

    def __init__(self):
        self.corners = [self.CORNER_NULL] * self.MAX_CORNER_AMOUNT

    def fill(self, side, value):
        '''
        填充边角
        :param side: 位置
        :param value: 值
        :return: 是否是新值
        '''
        if self.corners[side] != value:
            self.corners[side] = value
            return True
        else:
            return False

    def get(self, side):
        return self.corners[side]

    def is_side_empty(self, side):
        return self.get(side) == self.CORNER_NULL

    def __str__(self):
        return '[tl:%d, tr:%d, bl:%d, br:%d]' % tuple(self.corners)

    @property
    def tile(self):
        '''
        瓦片索引
        :return:
        '''
        tl = int(self.get(self.TOP_LEFT) != self.CORNER_NULL)
        tr = int(self.get(self.TOP_RIGHT) != self.CORNER_NULL)
        bl = int(self.get(self.BOTTOM_LEFT) != self.CORNER_NULL)
        br = int(self.get(self.BOTTOM_RIGHT) != self.CORNER_NULL)
        # 垂直镜像
        return  (br << 1) | (bl << 0) | (tr << 3) | (tl << 2)

    @property
    def filled(self):
        '''
        已填值集合
        :return:
        '''
        return set(filter(lambda x: x != self.CORNER_NULL, self.corners))

    @property
    def mixed(self):
        '''
        是否是混合地块
        :return:
        '''
        return len(self.filled) > 1

    @property
    def left(self):
        '''
        剩余未填充数量
        :return:
        '''
        null = filter(lambda x: x == self.CORNER_NULL, self.corners)
        return len(null)

    @property
    def empty(self):
        '''
        是否完全未填充
        :return:
        '''
        return self.left == self.MAX_CORNER_AMOUNT

    @property
    def partial(self):
        '''
        是否部分填充
        :return:
        '''
        return 0 < self.left < self.MAX_CORNER_AMOUNT

    @property
    def full(self):
        '''
        是否完整填充
        :return:
        '''
        return self.left == 0

class Cell(object):
    def __init__(self, position):
        self.position = position
        self.corner = Corner()

    def fill_corner(self, side, value):
        return self.corner.fill(side, value)

    def walkable(self, position):
        '''
        目标点是否可以行走到，网格分为四块中心点为(0,0)
        边界点
        (-0.5, -0.5) (-0.5, 0) (-0.5, 0.5)
         (0, -0.5)    (0, 0)    (0, 0.5)
        (0.5, -0.5)  (0.5, 0)   (0.5, 0.5)
        :param position: 目标点
        :return:
        '''
        overflow = 0.05
        delta_pos = position - self.position

        if not self.corner.is_side_empty(Corner.TOP_LEFT):
            if -0.5 <= delta_pos.column <= 0 \
                and -0.5 <= delta_pos.row <= 0:
                return True

        if not self.corner.is_side_empty(Corner.TOP_RIGHT):
            if 0 <= delta_pos.column <= 0.5 \
                and -0.5 <= delta_pos.row <= 0:
                return True

        if not self.corner.is_side_empty(Corner.BOTTOM_LEFT):
            if -0.5 <= delta_pos.column <= 0 \
                and 0 <= delta_pos.row <= 0.5:
                return True

        if not self.corner.is_side_empty(Corner.BOTTOM_RIGHT):
            if 0 <= delta_pos.column <= 0.5 \
                and 0 <= delta_pos.row <= 0.5:
                return True

        return False

    def __str__(self):
        return 'position=(%s), corner=(%s)' % (self.position, self.corner)