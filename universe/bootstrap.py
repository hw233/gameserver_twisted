# coding=utf-8
import universe
from manager import Creator, DataLoader, Layer, client
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
        self.creator = None
        self.random = None
        self.data_loader = None

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
            for outline in coll.outlines:
                outline.destroy()
            coll.outlines = []

        self.world.clear()

    def create_entity(self, layer, entity_data):
        entity = self.world.create_entity()
        self.layer.add_entity(layer, entity)

        comps = self.creator.create_components(entity_data)
        self.world.add_components(entity, *comps)
        return entity

    def create_entities(self, layer, entities_data):
        for data in entities_data:
            self.create_entity(layer, data)

    def create_biont_entity(self):
        biosphere = self.creator.create_biosphere(self.region, self.data)
        self.create_entities('biont', biosphere)

    def create_terrain_entity(self):
        # 创建区域
        self.region = self.creator.create_region(self.data)
        grid = self.region.grid()

        # 创建建筑
        buildings = self.creator.create_building(grid, self.data)
        self.create_entities('terrain', buildings)

        # 地图污点装饰
        spots = self.creator.create_spot(grid, self.data)
        self.create_entities('terrain', spots)

        # 创建地形
        terrains = self.creator.create_terrain(grid.tiles(), self.data)
        self.create_entities('terrain', terrains)

    def create_processor(self):
        # 创建形变处理器
        transform_processor = TransformProcessor()
        self.world.add_processor(transform_processor, priority=99)

        # 创建渲染处理器
        render_processor = RenderProcessor()
        self.world.add_processor(render_processor, priority=88)

        # 创建碰撞处理器
        collider_processor = ColliderProcessor()
        self.world.add_processor(collider_processor)

        # 创建动画处理器
        # animator_processor = AnimatorProcessor()
        # self.world.add_processor(animator_processor, priority=1)

    def create_player(self):
        entity = self.world.create_entity()
        self.layer.add_entity('player', entity)
        comps = self.creator.create_components(self.data['world']['player']['components'])
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

        # 创造生物
        self.create_biont_entity()

        # 创建处理器
        self.create_processor()

    def start(self, seed, finish_loading=None):
        # 设置伪随机
        self.random = PseudoRandom(seed)
        self.creator = Creator(self.random)
        self.data_loader = DataLoader(self.random)

        # 配置文件在种子设置之后，结果才能一致
        self.data = {
            "world": self.data_loader.load('world'),
            "landform": self.data_loader.load('landform'),
            "block": self.data_loader.load('block'),
            "tile": self.data_loader.load('tile'),
            "spot": self.data_loader.load('spot'),
            "building": self.data_loader.load('building'),
            "item": self.data_loader.load('item')
        }

        # 层管理
        self.layer = Layer(self, data=self.data['world']['layers'])

        # 创世
        self.create()

        # 降临
        self.world.start()


    def update(self):
        # self.world.update(self.timer.delta_time)
        self.timer.update()
        # client.camera_look_at()

    def set_player_position(self, position):
        '''
        设置玩家位置
        :param position:
        :return:
        '''
        transform = self.world.component_for_entity(self.player_entity, Transform)
        transform.position = position
        self.world.update(self.timer.delta_time)

    @client.only
    def player_occlusion_transparency(self):
        transform = self.world.component_for_entity(self.player_entity, Transform)

        ray_origin = transform.position + Vector3(0,100,0)
        ray_direction = Vector3().copy(client.get_scene().active_camera.position) - transform.position
        ray = Ray(ray_origin, ray_direction)

        for ent, (rend, coll) in self.world.get_components(Renderer, Collider):
            if coll.intersect(ray):
                rend.model.enable_instancing(False)
                rend.model.all_materials.transparent_mode = client.nexo_render.TRANSPARENT_MODE_ALPHA_R_Z
                rend.model.alpha = 50
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

    def terrain_move_limit(self, src_pos, dst_pos):
        '''
        地形移动限制
        :param src_pos: 当前位置
        :param dst_pos: 目标移动位置
        :return: 允许移动到的位置
        '''
        sh, _ = self.region.world_to_local(src_pos.x, dst_pos.z)
        _, sv = self.region.world_to_local(dst_pos.x, src_pos.z)
        dh, dv = self.region.world_to_local(dst_pos.x, dst_pos.z)

        if self.region.inside(round(dh), round(dv)):
            return Vector3(dst_pos.x, dst_pos.y, dst_pos.z)
        elif self.region.inside(round(sh), round(dv)):
            return Vector3(src_pos.x, dst_pos.y, dst_pos.z)
        elif self.region.inside(round(dh), round(sv)):
            return Vector3(dst_pos.x, dst_pos.y, src_pos.z)
        else:
            return Vector3(src_pos.x, src_pos.y, src_pos.z)

    def collision_move_limit(self, src_pos, dst_pos):
        collider = self.world.component_for_entity(self.player_entity, Collider)
        transform = self.world.component_for_entity(self.player_entity, Transform)

        transform.position = src_pos
        self.world.update(self.timer.delta_time)
        if collider.collisions:
            return dst_pos

        transform.position = dst_pos
        self.world.update(self.timer.delta_time)
        if not collider.collisions:
            return dst_pos

        transform.position = Vector3(dst_pos.x, dst_pos.y, src_pos.z)
        self.world.update(self.timer.delta_time)
        if not collider.collisions:
            return Vector3(dst_pos.x, dst_pos.y, src_pos.z)

        transform.position = Vector3(src_pos.x, dst_pos.y, dst_pos.z)
        self.world.update(self.timer.delta_time)
        if not collider.collisions:
            return Vector3(src_pos.x, dst_pos.y, dst_pos.z)

        return src_pos

    def outline_near_item(self, origin, radius=200):
        '''
        高亮附近可采集物体
        :return:
        '''
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
            client.outline(renderer, dist < radius)

    def approach(self, src_pos, dst_pos):
        '''
        玩家移动
        :param src_pos:
        :param dst_pos:
        :return:
        '''
        src_pos = Vector3().copy(src_pos)
        dst_pos = Vector3().copy(dst_pos)

        correct_pos = self.collision_move_limit(src_pos, dst_pos)
        correct_pos = self.terrain_move_limit(src_pos, correct_pos)

        # 设置玩家位置
        self.set_player_position(correct_pos)

        # 高亮附近可采集物体
        # self.outline_near_item(correct_pos)

        # 玩家遮挡透明
        # self.player_occlusion_transparency()

        return correct_pos

    def get_born_position(self):
        node = self.random.choice(self.region.get_nodes())
        x, z = self.region.local_to_world(node.horizontal, node.vertical)
        return [x, 0, z]

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

        if item and item.reapable:
            self.drop(tran.position, item.reaped)
        if item and item.droppable:
            self.drop(tran.position + Vector3(120, 0, -120), item.good)

        if rend and rend.model:
            if rend.model.has_anim_event('fall', 'end'):
                def end_drop(model, anim_name, key, data):
                    model.destroy()
                rend.model.stop_animation()
                rend.model.play_animation('fall')
                rend.model.register_anim_key_event('fall', 'end', end_drop)
            else:
                rend.model.destroy()

        self.world.delete_entity(entity)
        self.layer.remove(entity)
