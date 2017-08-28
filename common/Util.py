import math
import random


def unpack_id_pos(data_str):
    data = data_str.split(',')
    return [int(data[0]), float(data[1]), float(data[2]), float(data[3])]


def pack_id_pos_health(data):
    return str(data[0]) + ',%.3f' % data[1] + ',%.3f' % data[2] + ',%.3f' % data[3] + ',' + str(data[4])


def pack_id_pos_health_list_to_string(data):
    return '|'.join(pack_id_pos_health(x) for x in data)


def unpack_string_to_id_pos_list(s):
    return [unpack_id_pos(x) for x in s.split('|')]


def vector3_normalize(v):
    s = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    return [x / s for x in v]


def vector3_inner_product(v, num):
    if len(v) != 3:
        print "vector3_inner_product error"
        return None
    return [num * x for x in v]


def vector3_add(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print "vector3_add error"
        return None
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


def vector2_distance(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        print "vector2_distance error"
        return None
    s = (v1[0] - v2[0])**2 * (v1[1] - v2[1])**2
    return math.sqrt(s)


def vector3_distance(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print "vector3_distance error"
        return None
    s = 0
    for i in xrange(0, 3):
        s += (v1[i] - v2[i])**2
    return math.sqrt(s)


def vector3_equal(v1, v2):
    if math.fabs(v1[0] - v2[0]) > 1e-5:
        return False
    if math.fabs(v1[1] - v2[1]) > 1e-5:
        return False
    if math.fabs(v1[2] - v2[2]) > 1e-5:
        return False
    return True


def get_random_index_with_distribution(distribution):
    x = random.random()
    cnt = 0.0
    for i, d in enumerate(distribution):
        cnt += d
        if x < cnt:
            return i
