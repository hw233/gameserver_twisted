# coding=utf-8

from random import Random

class MapUtil(object):
    def __init__(self):
        self._random = Random()

    @property
    def random(self):
        return self._random

    def weight_choice(self, list, value_func=lambda x:x, weight_func=lambda x:x):
        '''
        带权重的随机
        :param list: 数据列表
        :param value_func: 取出列表数值项的函数
        :param weight_func: 去除列表权重项的函数
        :return: 选中的value
        '''
        total_weight = 0
        for item in list:
            total_weight += weight_func(item)
        rand_weight = self.random.randint(0, total_weight - 1)
        for item in list:
            rand_weight -= weight_func(item)
            if rand_weight < 0:
                return value_func(item)

    def grow_divide(self, current, target):
        '''
        生长分裂 越接近目标越容易分裂
        :param current:
        :param target:
        :return: True分裂 False不分裂
        '''
        r = self.random.uniform(0, 1) ** 0.5
        if r < current * 1.0 / target:
            return True
        else:
            return False

_inst = MapUtil()
weight_choice = _inst.weight_choice
random = _inst.random
grow_divide = _inst.grow_divide