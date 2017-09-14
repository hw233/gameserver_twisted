# coding=utf-8
import math

def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class Vector3(object):
    def __init__(self, x=.0, y=.0, z=.0):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return 'x=%f, y=%f, z=%f' % tuple(self.list)

    @property
    def list(self):
        return [self.x, self.y, self.z]

    def copy(self, src=None):
        if src is not None:
            self.x, self.y, self.z = src.x, src.y, src.z
            return self
        else:
            return Vector3().copy(self)

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
    def normalized(self):
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

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    # 求两个向量距离
    @staticmethod
    def distance(v1, v2):
        return (v1 - v2).magnitude

    @staticmethod
    def angle(from_v, to_v):
        return math.acos(Vector3.dot(from_v.normalized, to_v.normalized)) * 180 / math.pi

    @staticmethod
    def sign(val):
        if val == 0.0:
            return 0.0
        return 1 if val > 0 else -1

    @staticmethod
    def angle_to_axis(v, axis, up):
        axis = Vector3.forward()
        up = Vector3.up()
        normal = Vector3.cross(v, axis).normalized
        angle = - Vector3.angle(v, axis) * Vector3.sign(Vector3.dot(normal, up))
        return angle

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
