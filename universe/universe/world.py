# coding=utf-8

from processor import Processor

START_ENTITY_ID = 1000

class World:
    def __init__(self):
        self._next_entity_id = START_ENTITY_ID
        self._components = {}
        self._processors = []
        self._entities = {}
        self._new_entities = set()
        self._dead_entities = set()

    def clear(self):
        '''
        世界末日
        :return:
        '''
        self._next_entity_id = START_ENTITY_ID
        self._components = {}
        self._processors = []
        self._entities = {}
        self._dead_entities = set()

    def add_processor(self, processor_instance, priority=0):
        '''
        增加处理器
        :param processor_instance: 处理器实例，Processor
        :param priority: 优先级
        '''
        assert issubclass(processor_instance.__class__, Processor)
        processor_instance.priority = priority
        processor_instance.world = self
        self._processors.append(processor_instance)
        self._processors.sort(key=lambda proc: proc.priority, reverse=True)

    def remove_processor(self, processor_type):
        '''
        移除处理器
        :param processor_type: 处理器类型
        '''
        for processor in self._processors:
            if type(processor) == processor_type:
                processor.world = None
                self._processors.remove(processor)

    def get_processor(self, processor_type):
        '''
        获取一个处理器实例
        :param processor_type: 处理器类型
        '''
        for processor in self._processors:
            if type(processor) == processor_type:
                return processor

    def create_entity(self, *components):
        '''
        创建一个新实体
        :param components: 附带组件
        :return: id
        '''
        self._next_entity_id += 1

        for component in components:
            self.add_component(self._next_entity_id, component)

        self._new_entities.add(self._next_entity_id)

        return self._next_entity_id

    def delete_entity(self, entity, immediate=False):
        '''
        删除实体
        :param entity: 实体id
        :param immediate: 是否立即删除，立即删除可能引起正在进行的遍历错误
        :return:
        '''
        if immediate:
            for component_type in self._entities[entity]:
                self._components[component_type].discard(entity)

                if not self._components[component_type]:
                    del self._components[component_type]

            del self._entities[entity]

        else:
            self._dead_entities.add(entity)

    def component_for_entity(self, entity, component_type):
        '''
        通过实体获取指定类型的组件
        :param entity: 实体id
        :param component_type: 组件实体类型
        :return: 组件实例
        '''
        _entity = self._entities.get(entity)
        if _entity is None:
            return
        return _entity.get(component_type)

    def components_for_entity(self, entity):
        '''
        获取实体的所有组件
        :param entity: 实体id
        :return: 组件实例
        '''
        _entity = self._entities.get(entity)
        if _entity is None:
            return
        return tuple(_entity.values())

    def has_component(self, entity, component_type):
        '''
        检查实体是否含有指定类型的组件
        :param entity: 实体id
        :param component_type: 组件类型
        :return: 是否含有
        '''
        _entity = self._entities.get(entity)
        if _entity is None:
            return
        return component_type in _entity

    def add_component(self, entity, component_instance):
        '''
        往实体挂载组件
        :param entity: 实体id
        :param component_instance: 组件实例
        '''
        component_type = type(component_instance)
        if component_type not in self._components:
            self._components[component_type] = set()
        self._components[component_type].add(entity)

        if entity not in self._entities:
            self._entities[entity] = {}

        self._entities[entity][component_type] = component_instance

    def add_components(self, entity, *component_instances):
        '''
        批量挂载组件
        :param entity: 实体id
        :param component_instances: 组件实例组
        '''
        for component_instance in component_instances:
            self.add_component(entity, component_instance)

    def remove_component(self, entity, component_type):
        '''
        从实体移除组件
        :param entity: 实体id
        :param component_type: 组件类型
        '''
        self._components[component_type].discard(entity)

        if not self._components[component_type]:
            del self._components[component_type]

        del self._entities[entity][component_type]

        if not self._entities[entity]:
            del self._entities[entity]

        return entity

    def get_component(self, component_type):
        '''
        获取实体和组件的迭代器
        :param component_type: 组件类型
        :return: 迭代器 (实体, 组件)
        '''
        entity_db = self._entities
        for entity in self._components.get(component_type, []):
            yield entity, entity_db[entity][component_type]

    def get_components(self, *component_types):
        '''
        获取实体和组件组
        :param component_type: 组件类型
        :return: 迭代器 实体, (组件1, 组件2 ...)
        '''
        entity_db = self._entities
        comp_db = self._components

        try:
            for entity in set.intersection(*[comp_db[ct] for ct in component_types]):
                yield entity, [entity_db[entity][ct] for ct in component_types]
        except KeyError:
            pass

    def get_new_entities_components(self, *component_types):
        '''
        获取新实体和组件组
        :param component_type: 组件类型
        :return: 迭代器 实体, (组件1, 组件2 ...)
        '''
        entity_db = self._entities

        for entity in self._new_entities:
            try:
                components = [entity_db[entity][ct] for ct in component_types]
                yield entity, components
            except KeyError:
                pass

    def process(self, dt, *args, **kwargs):
        '''
        清理实体和批量调用处理器更新函数
        :param dt: delta time 单位秒
        :param args: 可选参数
        '''
        # 处理需要移除的实体
        if self._dead_entities:
            for entity in self._dead_entities:
                self.delete_entity(entity, immediate=True)
            self._dead_entities.clear()

        # 如果存在新实体则调用start方法
        if self._new_entities:
            for processor in self._processors:
                processor.start(*args, **kwargs)
            # 清空新实体
            self._new_entities.clear()

        # # 如果存在脏实体则调用start方法
        # if self._dirty_entities:
        #     for processor in self._processors:
        #         processor.update(dt, *args)
        #     # 清空脏实体
        #     self._dirty_entities.clear()