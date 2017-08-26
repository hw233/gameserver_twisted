# coding=utf-8

import math

class GridPosition(object):
    '''
    单元格
    '''
    def __init__(self, row=0, column=0):
        self.row = row
        self.column = column

    def relate_to(self, other):
        '''
        绝对转相对坐标
        :return:
        '''
        return GridPosition(self.row - other.row, self.column - other.column)

    def absolute_by(self, other):
        '''
        相对转绝对坐标
        :return:
        '''
        return GridPosition(self.row + other.row, self.column + other.column)

    @property
    def magnitude(self):
        return math.sqrt(self.row * self.row + self.column * self.column)

    def distance_to(self, other):
        return (self - other).magnitude

    def __add__(self, other):
        return GridPosition(self.row + other.row, self.column + other.column)

    def __sub__(self, other):
        return GridPosition(self.row - other.row, self.column - other.column)

    def __str__(self):
        return 'row=%s, column=%s' % (str(self.row), str(self.column))

    def translate(self, row, column):
        return GridPosition(self.row + row, self.column + column)

class Vector3(object):
    x = .0
    y = .0
    z = .0

    def __init__(self, x=.0, y=.0, z=.0, obj=None):
        if isinstance(x, Vector3):
            self.x, self.y, self.z = x.x, x.y, x.z
        elif obj is not None:
            self.x, self.y, self.z = obj.x, obj.y, obj.z
        else:
            self.x, self.y, self.z = x, y, z

    def __str__(self):
        return 'x=%f, y=%f, z=%f' % tuple(self.list)

    @property
    def list(self):
        return [self.x, self.y, self.z]

    def copy(self, src):
        self.x, self.y, self.z = src.x, src.y, src.z
        return self

    # 加法
    def __add__(self, obj):
        return Vector3(self.x + obj.x, self.y + obj.y, self.z + obj.z)

    # 减法
    def __sub__(self, obj):
        return Vector3(self.x - obj.x, self.y - obj.y, self.z - obj.z)

    # 乘常数
    def __mul__(self, value):
        return Vector3(self.x * value, self.y * value, self.z * value)

    # 除以常数
    def __div__(self, value):
        return Vector3(self.x / value, self.y / value, self.z / value)

    # 向量的模
    @property
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    # 归一化
    @property
    def normalize(self):
        return Vector3(self.x, self.y, self.z) / self.magnitude

    @staticmethod
    def zero():
        return Vector3(0, 0, 0)

    @staticmethod
    def forward():
        return Vector3(0, 0, 1)

    @staticmethod
    def up():
        return Vector3(0, 1, 0)

    @staticmethod
    def right():
        return Vector3(1, 0, 0)

    # 线性插值
    @staticmethod
    def lerp(start, goal, t):
        if t < 0:
            return Vector3().copy(start)
        elif t > 1:
            return Vector3().copy(goal)
        return  start + (goal - start) * t

    @staticmethod
    def cross(v1, v2):
        return Vector3(v1.y * v2.z - v2.y * v1.z, v1.z * v2.x - v1.x * v2.z,
                       v1.x * v2.y - v2.x * v1.y)

    # 求两个向量距离
    @staticmethod
    def distance(v1, v2):
        return (v1 - v2).magnitude

class Vector2:
    x = .0
    y = .0

    def __init__(self, x=.0, y=.0, obj=None):
        if isinstance(x, Vector2):
            self.x, self.y = x.x, x.y
        elif obj is not None:
            self.x, self.y = obj.x, obj.y
        else:
            self.x, self.y = x, y

    def __str__(self):
        return 'x=%f, y=%f' % tuple(self.list)

    @property
    def list(self):
        return [self.x, self.y]

    def copy(self, src):
        self.x, self.y = src.x, src.y
        return self

    # 加法
    def __add__(self, obj):
        return Vector2(self.x + obj.x, self.y + obj.y)

    # 减法
    def __sub__(self, obj):
        return Vector2(self.x - obj.x, self.y - obj.y)

    # 乘常数
    def __mul__(self, value):
        return Vector2(self.x * value, self.y * value)

    # 除以常数
    def __div__(self, value):
        return Vector2(self.x / value, self.y / value)

    # 向量的模
    @property
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    # 归一化
    @property
    def normalize(self):
        return Vector2(self.x, self.y) / self.magnitude

    @staticmethod
    def zero():
        return Vector2(0, 0)

    # 线性插值
    @staticmethod
    def lerp(start, goal, t):
        if t < 0:
            return Vector2().copy(start)
        elif t > 1:
            return Vector2().copy(goal)
        return  start + (goal - start) * t

    # 求两个向量距离
    @staticmethod
    def distance(v1, v2):
        return (v1 - v2).magnitude

class Ray(object):

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

class AABB(object):
    def __init__(self, left_bottom_backward, right_top_forward):
        self.min = left_bottom_backward
        self.max = right_top_forward


class Physics(object):
    def __init__(self):
        pass

    def ray_aabb_intersect(self, ray, aabb):
        '''
        射线与AABB是否相交
        :param ray: 射线
        :param aabb: 碰撞盒
        :return: 是否相交
        '''
        # 预计算方向分量倒数，避免大量除法
        dir_fraction = Vector3(1.0 / ray.direction.x, 1.0 / ray.direction.y, 1.0 / ray.direction.z)

        # t1 = (aabb.min - ray.origin) *

        t1 = (aabb.min.x - ray.origin.x) * dir_fraction.x
        t2 = (aabb.max.x - ray.origin.x) * dir_fraction.x
        t3 = (aabb.min.y - ray.origin.y) * dir_fraction.y
        t4 = (aabb.max.y - ray.origin.y) * dir_fraction.y
        t5 = (aabb.min.y - ray.origin.z) * dir_fraction.z
        t6 = (aabb.max.y - ray.origin.z) * dir_fraction.z
        t_min = max(min(t1, t2), min(t3, t4), min(t5, t6))
        t_max = min(max(t1, t2), max(t3, t4), max(t5, t6))

        dis = 0

        # 在背后
        if t_max < 0:
            return False

        # 不相交
        if t_min > t_max:
            return False

        return True
