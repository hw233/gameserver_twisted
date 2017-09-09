# coding=utf-8

class Layer(object):
    def __init__(self, universe, data=None):
        self.world = universe.world
        self._altitudes = {}
        self._layers = {}
        if data is not None:
            for name, layer in data.iteritems():
                self._layers.setdefault(name, [])
                self._altitudes.setdefault(name, layer['altitude'])
                # 预制体
                for preset_data in layer['presets']:
                    comps = universe.creator.create_components(preset_data)
                    entity = self.world.create_entity()
                    self.world.add_components(entity, *comps)


    def altitude(self, layer):
        return self._altitudes.get(layer, 0)

    @property
    def merged_creatures(self):
        return reduce(lambda a, b: a + b, sorted(self._layers.values()))

    def add_entity(self, layer, entity):
        '''
        增加实体到层
        :param layer: 层名称
        :param entity:实体id
        '''
        container = self._layers.setdefault(layer, [])
        container.append(entity)

    def get_entities(self, layer):
        '''
        获取层内的所有对象
        :param layer: 层名称
        :return: 对象集合
        '''
        return self._layers.get(layer, [])

    def remove(self, entity):
        '''
        层移除实例
        :param entity: 实体id
        '''
        for container in sorted(self._layers.itervalues()):
            if entity in container:
                container.remove(entity)

