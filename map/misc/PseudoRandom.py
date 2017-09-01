# coding=utf-8

from random import Random

def weight_choice(self, list, value=None, weight=None):
    '''
    带权重的随机
    :param list: 数据列表
    :param value: 取出列表数值项的函数
    :param weight: 去除列表权重项的函数
    :return: 选中的value
    '''
    if value is None:
        value = lambda x: x

    if weight is None:
        weight = lambda x: x

    total_weight = 0
    for item in list:
        total_weight += weight(item)
    rand_weight = self.randint(0, total_weight - 1)
    for item in list:
        rand_weight -= weight(item)
        if rand_weight < 0:
            return value(item)


def grow_divide(self, current, target):
    '''
    生长分裂 越接近目标越容易分裂
    :param current:
    :param target:
    :return: True分裂 False不分裂
    '''
    r = self.uniform(0, 1) ** 0.5
    if r < current * 1.0 / target:
        return True
    else:
        return False

class PseudoRandom(object):
    def __init__(self):
        self._randoms = {}

    def get(self, id=0):
        if self._randoms.get(id) is None:
            Random.weight_choice = weight_choice
            Random.grow_divide = grow_divide
            self._randoms[id] = Random()

        return self._randoms[id]

    def set(self, seed=None, id=0):
        self.get(id).seed(seed)


_inst = PseudoRandom()
get = _inst.get
set = _inst.set