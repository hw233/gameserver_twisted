# coding=utf-8

'''
面积约束
'''
class AreaRule(object):

    def __init__(self, target_area):
        '''
            初始化
        :param target_area: 目标面积
        '''
        if target_area <= 0:
            raise ValueError('Target area must > zero')

        self.area = 0       # 当前面积计数器
        self.target_area = target_area

    def increase(self, delta_area=1.0):
        '''
        增加面积
        :return:
        '''
        self.area += delta_area

    @property
    def validated(self):
        '''
        是否满足面积约束
        :return:
        '''
        return self.area <= self.target_area

'''
形状约束
'''
class ShapeRule(object):

    @staticmethod
    def like_circle(center, point, radius):
        '''
        类似圆形
        :return: bool 是否符合图形要求
        '''
        delta = center - point
        if (delta.row ** 2 + delta.column ** 2) < radius ** 2:
            return True
        else:
            return False

    @staticmethod
    def like_rectangle(width, height):
        '''
        类似矩形
        :return:
        '''
        pass
