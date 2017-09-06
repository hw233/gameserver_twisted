# coding=utf-8
import universe
from manager import Creator, Data, Layer, client
from misc import PseudoRandom, Vector3, Ray
from component import Renderer, Transform, Collider, Item
from processor import RenderProcessor, AnimatorProcessor, TransformProcessor, ColliderProcessor

class Universe(object):
    def __init__(self):
        self.world = universe.World()
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
            grid_vertices = debug.create_grid_line(200, 200, 200, 200)
            self.world.add_components(
                grid_entity,
                Renderer(gim=grid_vertices),
                Transform()
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

    def create_entity(self, layer, entity_data):
        entity = self.world.create_entity()
        self.layer.add_entity(layer, entity)

        comps = Creator.create_components(entity_data)
        self.world.add_components(entity, *comps)
        return entity

    def create_entities(self, layer, entities_data):
        for data in entities_data:
            self.create_entity(layer, data)

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
            horizontal=0,
            vertical=1,
            value=1
        ))

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

        # 创建建筑
        buildings = Creator.create_building(grid, self.data)
        self.create_entities('terrain', buildings)

        # 地图污点装饰
        spots = Creator.create_spot(grid, self.data)
        self.create_entities('terrain', spots)

        # 创建地形
        terrains = Creator.create_terrain(grid.tiles, self.data)
        self.create_entities('terrain', terrains)

    def create_processor(self):
        # 创建形变处理器
        transform_processor = TransformProcessor()
        self.world.add_processor(transform_processor, priority=99)

        # 创建渲染处理器
        render_processor = RenderProcessor()
        self.world.add_processor(render_processor, priority=88)

        # 创建碰撞处理器
        # collider_processor = ColliderProcessor()
        # self.world.add_processor(collider_processor)

        # 创建动画处理器
        animator_processor = AnimatorProcessor()
        self.world.add_processor(animator_processor, priority=1)

    def create_player(self):
        entity = self.world.create_entity()
        self.layer.add_entity('player', entity)
        comps = Creator.create_components([
            {
                'comp': 'transform'
            }
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

    def start(self, seed, finish_loading=None):
        # 设置伪随机
        PseudoRandom.set(seed)
        # 配置文件在种子设置之后，结果才能一致
        self.data = {
            "world": Data.load('world'),
            "landform": Data.load('landform'),
            "block": Data.load('block'),
            "tile": Data.load('tile'),
            "spot": Data.load('spot'),
            "building": Data.load('building'),
            "item": Data.load('item')
        }

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
        ray_direction = Vector3().copy(client.get_scene().active_camera.position) - transform.position
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
        return entity, renderer.model if renderer else None, item


    def get_target_entity(self, origin, radius=200):
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
        entities = self.layer.get_entities('drop') + self.layer.get_entities('biont')
        for entity in entities:
            transform = self.world.component_for_entity(entity, Transform)
            renderer = self.world.component_for_entity(entity, Renderer)
            item = self.world.component_for_entity(entity, Item)
            if item is None or item.none:
                continue
            item_pos = transform.position
            origin_pos = Vector3().copy(origin)
            dist = Vector3.distance(origin_pos, item_pos)
            if dist < min_dist and dist < radius:
                min_dist = dist
                target_renderer = renderer
                target_item = item
                target_entity = entity

        return target_entity, target_renderer.model if target_renderer else None, target_item


    def correct_moving(self, src_pos, dst_pos):
        '''
        修正移动
        :param src_pos:
        :param dst_pos:
        :return:
        '''
        src = Vector3().copy(src_pos)
        dst = Vector3().copy(dst_pos)
        dh = dst.x / self.data['world']['tile']['width']
        dv = dst.z / self.data['world']['tile']['length']
        if self.region.inside(dh, dv):
            return dst_pos
        else:
            return src_pos

    def approach(self, src_pos, dst_pos):
        '''
        玩家移动
        :param src_pos:
        :param dst_pos:
        :return:
        '''

        correct_pos = self.correct_moving(src_pos, dst_pos)

        # 设置玩家位置
        self.set_player_position(Vector3(correct_pos.x, correct_pos.y, correct_pos.z))

        # 玩家遮挡透明
        # self.player_occlusion_transparency()
        # return correct_pos
        return dst_pos

    def drop(self, position, good):
        '''
        掉落
        :param position: 生成位置
        :param good: 物品
        '''
        comps_data = [{
            'comp': 'transform',
            'position': {
                'x': position.x,
                'y': position.y,
                'z': position.z
            }
        }]

        if type(good) == int or type(good) == str:
            # 新掉落物品
            comps_data += self.data['item'].get(good, {}).get('components', [])
        else:
            # 玩家丢出物品
            comps_data += self.data['item'].get(good.item, {}).get('components', [])
            for comp in comps_data:
                if comp.get('comp') == 'item':
                    comp['good'] = good

        self.create_entity('drop', comps_data)
        self.world.start()

    def reap(self, entity, damage):
        '''
        砍伐收集
        :param entity:
        :param damage:
        :return:
        '''
        item = self.world.component_for_entity(entity, Item)
        if item.hittable:
            item.take_damage(damage)

    def destroy(self, entity):
        item = self.world.component_for_entity(entity, Item)
        tran = self.world.component_for_entity(entity, Transform)
        rend = self.world.component_for_entity(entity, Renderer)
        if rend and rend.model:
            if rend.model.has_anim_event('fall', 'end'):
                def end_drop(model, anim_name, key, *data):
                    model.destroy()
                rend.model.stop_animation()
                rend.model.play_animation('fall')
                rend.model.register_anim_key_event('fall', 'end', end_drop)
            else:
                rend.model.destroy()


        if item and item.reapable:
            self.drop(tran.position, item.reaped)
        if item and item.droppable:
            self.drop(tran.position + Vector3(120, 0, -120), item.good)

        self.world.delete_entity(entity)
        self.layer.remove(entity)
