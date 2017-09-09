# coding=utf-8

'''
数据内标签
  @ 调用方法
  # 引用数据
'''

class DataLoader(object):

    def __init__(self, random):
        self.random = random
        self.actions = {
            "rand.int": lambda a, b: self.random.randint(a, b),
            "rand.float": lambda a, b: self.random.uniform(a, b)
        }

    def load(self, module, section=None):
        origin = __import__('universe.data.%s_data' % module, globals(), locals(), ["data"]).data
        if section is not None:
            origin = origin[section]
        data = self._convert(origin)
        return data

    def _action(self, method, param):
        '''
        调用函数
        :return:
        '''
        if type(param) == tuple:
            return self.actions[method](*param)
        elif type(param) == dict:
            return self.actions[method](**param)
        else:
            return self.actions[method](param)

    def _convert(self, data):
        '''
        数据转换
        '''

        if type(data) == list:
            new_list = []
            for val in data:
                new_list.append(self._convert(val))
            return new_list

        elif type(data) == dict:
            new_dict = {}
            for key, val in sorted(data.items()):
                if "@" in str(key):
                    # 处理函数调用
                    name, method = str(key).replace(' ', '').split('@', 2)
                    new_dict[name] = self._action(method, val)

                elif str(key).startswith('#'):
                    # 以#开头则直接更新父级
                    ref = str(key)[1:]
                    new_dict.update(self.load(ref, val))

                elif "#" in str(key):
                    # 处理数据引用
                    name, ref = str(key).replace(' ', '').split('#', 2)
                    new_dict[name] = self.load(ref, val)

                else:
                    # 普通转换
                    new_dict[key] = self._convert(val)

            return new_dict

        else:
            return data
