# coding=utf-8

from random import Random

class PseudoRandom(object):
    def __init__(self, seed=None):
        self._random = Random(seed)

    def seed(self, seed):
        self._random.seed(seed)

    def random(self):
        return self._random.random()

    def randint(self, a, b):
        return self._random.randint(a, b)

    def uniform(self, a, b):
        return self._random.uniform(a, b)

    def choice(self, seq):
        return self._random.choice(seq)

    def gauss(self, mu, sigma):
        return self._random.gauss(mu, sigma)

    def grow_stop(self, current, target, exponential=1):
        '''
        生长停止 越接近目标越容易停止
        :param current:
        :param target:
        :return: True分裂 False不分裂
        '''
        r = self._random.uniform(0, 1) ** exponential
        if r < current * 1.0 / target:
            return True
        else:
            return False

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
        rand_weight = self._random.randint(0, total_weight - 1)
        for item in list:
            rand_weight -= weight(item)
            if rand_weight < 0:
                return value(item)



    def random_pass(self, a):
        '''
        连
        :param a: 阈值
        :return: uniform小于a则返回True
        '''
        return self._random.random() <= a