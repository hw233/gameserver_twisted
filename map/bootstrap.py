# coding=utf-8
import universe
from manager import Creator, Data, Layer, client
from misc import PseudoRandom, Vector3, Ray
from component import Renderer, Transform, Collider, Item
from processor import RenderProcessor, AnimatorProcessor, TransformProcessor, ColliderProcessor

class Universe(object):
    def __init__(self):
        self.world = None
        self.region = None
        self.layer = None
        self.timer = universe.Timer()
        self.data = {}
        self.player_entity = None

    @client.only
    def debug(self):
        from manager import debug
        if self.data['world']['debug']['grid']['visible']:
            grid_entity = self.world.create_entity()
            grid_primitive = debug.create_grid_line(200, 200, 200, 200)
            self.world.add_component(
                grid_entity,
                Renderer(primitive=grid_primitive)
            )

    def clear(self):
        for entity, rend in self.world.get_component(Renderer):
            if rend.model:
                rend.model.destroy()
                rend.model = None

        for entity, coll in self.world.get_component(Collider):
            if coll.outline:
                coll.outline.destroy()
                coll.outline = None
        self.world.clear()

    def create_entities(self, layer, entities_data):
        for data in entities_data:
            entity = self.world.create_entity()
            self.layer.add_entity(layer, entity)

            comps = Creator.create_components(data)
            self.world.add_components(entity, *comps)

    def create_biont_entity(self):
        biosphere = Creator.create_biosphere(self.region, self.data)
        self.create_entities('biont', biosphere)

    def create_test_terrain(self):
        # 创建区域
        from manager import graph
        self.region = graph.Region()
        self.region.add_node(graph.Node(
            horizontal=0,
            vertical=0,
            value=1
        ))
        self.region.add_node(graph.Node(
            horizontal=1,
            vertical=1,
            value=1
        ))
        self.region.add_node(graph.Node(
            horizontal=0,
            vertical=1,
            value=2
        ))


        for tile in self.region.grid().tiles:
            print tile.value()

        terrains = Creator.create_terrain(self.region.grid().tiles, self.data)
        for tile_data in terrains:
            # 创建实体并加入层
            entity = self.world.create_entity()
            self.layer.add_entity('terrain', entity)

            comps = Creator.create_components(tile_data)
            self.world.add_components(entity, *comps)

    def create_terrain_entity(self):
        # 创建区域
        self.region = Creator.create_region(self.data['block'])
        grid = self.region.grid()

        print 'create_building', PseudoRandom.get().random()

        # 创建建筑
        buildings = Creator.create_building(grid, self.data)
        self.create_entities('terrain', buildings)

        print 'create_spot', PseudoRandom.get().random()
        # 地图污点装饰
        spots = Creator.create_spot(grid, self.data)
        self.create_entities('terrain', spots)

        print 'create_terrain', PseudoRandom.get().random()
        # 创建地形
        terrains = Creator.create_terrain(grid.tiles, self.data)
        self.create_entities('terrain', terrains)

    def create_processor(self):
        # 创建渲染处理器
        render_processor = RenderProcessor()
        self.world.add_processor(render_processor)

        # 创建形变处理器
        transform_processor = TransformProcessor()
        self.world.add_processor(transform_processor)

        # 创建碰撞处理器
        # collider_processor = ColliderProcessor()
        # self.world.add_processor(collider_processor)

        # 创建动画处理器
        animator_processor = AnimatorProcessor()
        self.world.add_processor(animator_processor)

    def create_player(self):
        entity = self.world.create_entity()
        self.layer.add_entity('player', entity)
        comps = Creator.create_components([
            {
                'comp': 'transform',
                'position': {
                    'x': 0, 'y': 0, 'z': 0
                }
            },
            # {
            #     'comp': 'collider',
            #     'type': 'AABB',
            #     'shape': {
            #         'width': 60,
            #         'height': 100,
            #         'length': 60
            #     },
            #     'center': {
            #         'x': 0, 'y': 100, 'z': 0
            #     },
            #     'outline_visible': True
            # }
        ])
        self.world.add_components(entity, *comps)
        self.player_entity = entity

    def create(self):
        '''
        创世
        '''
        # 调试功能
        self.debug()

        # 创建虚拟玩家
        self.create_player()

        # 创造地形
        self.create_terrain_entity()
        # self.create_test_terrain()

        # 创造生物
        self.create_biont_entity()

        # 创建处理器
        self.create_processor()

    def start(self, seed):
        # 设置伪随机
        PseudoRandom.set(seed)
        # 配置文件再种子设置之后，结果才能一致
        self.data = {
            "world": Data.load('world'),
            "landform": Data.load('landform'),
            "block": Data.load('block'),
            "tile": Data.load('tile'),
            "spot": Data.load('spot'),
            "building": Data.load('building')
        }
        print self.data['block'][0]['area']
        # 预创世
        self.world = universe.World()

        # 层管理
        self.layer = Layer(self.world, data=self.data['world']['layers'])

        # 创世
        self.create()

        # 降临
        self.world.start()

    def update(self):
        self.world.update(self.timer.delta_time)
        self.timer.update()

    def set_player_position(self, position):
        '''
        设置玩家位置
        :param position:
        :return:
        '''
        transform = self.world.component_for_entity(self.player_entity, Transform)
        transform.position = position

    @client.only
    def player_occlusion_transparency(self):

        transform = self.world.component_for_entity(self.player_entity, Transform)

        ray_origin = transform.position + Vector3(0,100,0)
        ray_direction = Vector3().copy(client.scene.active_camera.position) - transform.position
        ray = Ray(ray_origin, ray_direction)

        for ent, (rend, coll) in self.world.get_components(Renderer, Collider):
            if coll.collider.intersect(ray):
                rend.model.enable_instancing(False)
                rend.model.all_materials.transparent_mode = client.nexo_render.TRANSPARENT_MODE_ALPHA_R_Z
                rend.model.alpha = 100
            else:
                rend.model.enable_instancing(True)
                rend.model.all_materials.transparent_mode = client.nexo_render.TRANSPARENT_MODE_UNSET
                rend.model.alpha = 255

    def get_entity(self, entity):
        renderer = self.world.component_for_entity(entity, Renderer)
        item = self.world.component_for_entity(entity, Item)
        return {
            'id': entity,
            'model': renderer.model,
            'item': item
        }

    def get_target_entity(self, origin, radius):
        '''
        获取目标物体，为指定范围内的最近物体
        :param origin: 原点
        :param radius: 探测半径
        :return:
        '''
        min_dist = float('inf'),
        target_renderer = None
        target_item = None
        target_entity = None
        entities = self.layer.get_entities('biont')
        for entity in entities:
            transform = self.world.component_for_entity(entity, Transform)
            renderer = self.world.component_for_entity(entity, Renderer)
            item = self.world.component_for_entity(entity, Item)
            item_pos = transform.position
            origin_pos = Vector3().copy(origin)
            dist = Vector3.distance(origin_pos, item_pos)
            if dist < min_dist and dist < radius:
                min_dist = dist
                target_renderer = renderer
                target_item = item
                target_entity = entity

        print  target_entity

        if target_entity:
            return {
                'id': target_entity,
                'model': target_renderer.model if target_renderer else None,
                'item': target_item
            }
        else:
            return None


    def correct_moving(self, src_pos, dst_pos):
        '''
        修正移动
        :param src_pos:
        :param dst_pos:
        :return:
        '''
        src = Vector3().copy(src_pos)
        dst = Vector3().copy(dst_pos)


    def approach(self, src_pos, dst_pos):
        '''
        玩家移动
        :param src_pos:
        :param dst_pos:
        :return:
        '''

        # 设置玩家位置
        self.set_player_position(Vector3(src_pos.x, src_pos.y, src_pos.z))

        # 玩家遮挡透明
        # self.player_occlusion_transparency()


    def reap(self, entity, damage):
        item = self.world.component_for_entity(entity, Item)
        if item.hittable:
            item.take_damage(damage)
        print 'reap', damage

    def destroy(self, entity):
        print 'destroy'
        renderer = self.world.component_for_entity(entity, Renderer)
        if renderer.model:
            renderer.model.stop_animation()
            renderer.model.play_animation('fall')
            # renderer.model.destroy()
        self.world.delete_entity(entity)
        self.layer.remove(entity)

    @client.only
    def client_reap(self, entity):
        print 'client_reap'
        pass

    @client.only
    def client_collect(self, entity):
        print 'client collect'
        pass