# coding=utf-8
from map.misc import PseudoRandom

'''
数据内标签
  @ 调用方法
  # 引用数据
'''

ACTIONS = {
    "rand.int": lambda a, b: PseudoRandom.get().randint(a, b),
    "rand.float": lambda a, b: PseudoRandom.get().uniform(a, b)
}

class Data(object):

    @staticmethod
    def load(module, section=None):
        origin = __import__('map.map_data.%s_data' % module, globals(), locals(), ["data"]).data
        if section is not None:
            origin = origin[section]
        data = Data._convert(origin)
        return data

    @staticmethod
    def _action(method, param):
        '''
        调用函数
        :return:
        '''
        if type(param) == tuple:
            return ACTIONS[method](*param)
        elif type(param) == dict:
            return ACTIONS[method](**param)
        else:
            return ACTIONS[method](param)

    @staticmethod
    def _convert(data):
        '''
        数据转换
        '''

        if type(data) == list:
            new_list = []
            for val in data:
                new_list.append(Data._convert(val))
            return new_list

        elif type(data) == dict:
            new_dict = {}
            for key, val in sorted(data.items()):
                if "@" in str(key):
                    # 处理函数调用
                    name, method = str(key).replace(' ', '').split('@', 2)
                    new_dict[name] = Data._action(method, val)

                elif str(key).startswith('#'):
                    # 以#开头则直接更新父级
                    ref = str(key)[1:]
                    new_dict.update(Data.load(ref, val))

                elif "#" in str(key):
                    # 处理数据引用
                    name, ref = str(key).replace(' ', '').split('#', 2)
                    new_dict[name] = Data.load(ref, val)

                else:
                    # 普通转换
                    new_dict[key] = Data._convert(val)

            return new_dict

        else:
            return data
