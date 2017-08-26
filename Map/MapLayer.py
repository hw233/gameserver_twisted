# coding=utf-8

from MapItem import MapItem
from MapMath import Vector3

class MapLayerManager(object):

    def __init__(self):
        self._layers = []
        self._layers_dict = {}

    @property
    def all(self):
        return self._layers

    def get_layer(self, layer):
        if type(layer) == str:
            return self._layers_dict[layer]
        elif type(layer) == int:
            return self._layers[layer]
        elif isinstance(layer, MapLayer):
            return self._layers_dict[layer.name]

    def add_layer(self, layer):
        self._layers.append(layer)
        self._layers_dict[layer.name] = layer

    def remove_layer(self, layer):
        if isinstance(layer, MapLayer):
            # 通过实例删除
            self._layers.remove(layer)
            if hasattr(self._layers_dict, layer.name):
                del self._layers_dict[layer.name]

        elif type(layer) == str:
            # 通过名字删除
            self._layers = filter(lambda x: x.name != layer, self._layers)
            del self._layers_dict[layer.name]

class MapLayer(object):
    def __init__(self, name, y):
        '''
        层
        :param name: 名称
        :param y: y轴偏移
        '''
        self.name = name
        self._items = []
        self._y = y

    @property
    def y(self):
        return self._y

    @property
    def items(self):
        return self._items

    def add_item(self, item):
        self._items.append(item)

    def get_item(self, item):
        if type(item) == int:
            for x in self.items:
                if x.id == item:
                    return x

    def remove_item(self, item):
        if isinstance(item, MapItem):
            # 通过实例删除
            self._items.remove(item)

        elif type(item) == int:
            # 通过id删除
            self._items = filter(lambda x: x.id != item, self._items)
