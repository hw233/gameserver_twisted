# coding=utf-8
from mathematics import Vector3, is_close

class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized


class Sphere(object):
    def __init__(self):
        pass

class Capsule(object):
    def __init__(self):
        pass

class AABB(object):
    def __init__(self, min_point, max_point):
        self._min_point = min_point
        self._max_point = max_point
        self.position = Vector3()

    @property
    def min_point(self):
        return self._min_point + self.position

    @property
    def max_point(self):
        return self._max_point + self.position

    @property
    def min_x(self):
        return self.min_point.x

    @property
    def min_y(self):
        return self.min_point.y

    @property
    def min_z(self):
        return self.min_point.z

    @property
    def max_x(self):
        return self.max_point.x

    @property
    def max_y(self):
        return self.max_point.y

    @property
    def max_z(self):
        return self.max_point.z

    def intersect_ray(self, ray):
        t_near = float("-inf")
        t_far = float("inf")

        for axis in ['x', 'y', 'z']:
            r_ori = getattr(ray.origin, axis)
            r_dir = getattr(ray.direction, axis)
            min_p = getattr(self.min_point, axis)
            max_p = getattr(self.max_point, axis)

            if is_close(r_dir, 0):
                if (r_ori < min_p or r_ori > max_p):
                    return False
            else:
                t1 = (min_p - r_ori) / r_dir
                t2 = (max_p - r_ori) / r_dir
                t_near = max(t_near, min(t1, t2))
                t_far = min(t_far, max(t1, t2))


        if t_near > t_far or t_far < 0:
            return False

        return True

    def intersect_aabb(self, aabb):
        return not(
            self.min_point.x >= aabb.max_point.x or
            self.min_point.y >= aabb.max_point.y or
            self.min_point.z >= aabb.max_point.z or
            self.max_point.x <= aabb.min_point.x or
            self.max_point.y <= aabb.min_point.y or
            self.max_point.z <= aabb.min_point.z
        )

    def intersect(self, other):
        if isinstance(other, Ray):
            return self.intersect_ray(other)
        elif isinstance(other, AABB):
            return self.intersect_aabb(other)



class OBB(object):
    def __init__(self):
        pass