# coding=utf-8

from universe.misc import Vector3
from rule import AreaRule
import graph

class Creator(object):

    def __init__(self, random):
        self.random = random

    # ============ Environment ============

    def create_block(self, region, origin, data):
        '''
        创建区域
        :return:
        '''

        # 检查是否可以互相连接
        def check_socket(horizontal, vertical, key, sockets):
            for offset in graph.OFFSET_AROUND:
                h = horizontal + offset[0]
                v = vertical + offset[1]
                node = region.get_node(h, v)
                if node and (node.value != key and node.value not in sockets):
                    return False
            return True

        # 面积约束
        area_rule = AreaRule(data['area'])
        origin.value = data['landform']['id']
        task = [origin]
        while task and area_rule.validated:
            current = self.random.choice(task)
            task.remove(current)

            # 邻边扩张
            for direction in graph.NEIGHBORS:
                further = current.neighbour(direction)
                further.value = data['landform']['id']
                if region.get_node(further.horizontal, further.vertical) is None:
                    if check_socket(further.horizontal, further.vertical, current.value, data['sockets']):
                        region.add_node(further)
                        area_rule.increase()
                        if not area_rule.validated:
                            break
                        task.append(further)

    def create_region(self, data):
        region = graph.Region(horizontal_scale=data['world']['tile']['width'],
                              vertical_scale=data['world']['tile']['length'])

        def find_origin(region, radian):
            border_nodes = region.border_nodes
            min_diff = float('inf')
            min_h, min_v = 0, 0
            for node in border_nodes:
                diff = Vector3.angle(
                    Vector3(node.horizontal, 0, node.vertical),
                    Vector3(math.cos(radian), 0, math.sin(radian))
                )
                if diff < min_diff:
                    min_diff = diff
                    min_h, min_v = node.horizontal, node.vertical

            for offset in graph.OFFSET_NEIGHBORS:
                if region.get_node(min_h + offset[0], min_v + offset[1]) is None:
                    return graph.Node(min_h + offset[0], min_v + offset[1])

        import math
        current_radian = self.random.uniform(0, 2 * math.pi)
        step_radian = 2 * math.pi / (len(data['block']) - 1)
        for idx, block_data in enumerate(data['block']):
            if idx == 0:
                # 中心城区
                origin = graph.Node(horizontal=0, vertical=0)
                self.create_block(region, origin, block_data)
            else:
                # 其他地块
                origin = find_origin(region, current_radian)
                if origin:
                    self.create_block(region, origin, block_data)
                current_radian += step_radian
        return region

    def create_tile(self, tile, tile_data, landform_data):
        '''
        根据地块边角选择地形模型
        :param tile:
        :param tile_data:
        :param landform_data:
        :return:
        '''
        key = tile.major
        if tile.mixed:
            # 过渡地块
            pri_major = landform_data[tile.major]['priority']
            pri_secondary = landform_data[tile.secondary]['priority']
            landform_id = landform_data[tile.major]['transition'][tile.secondary]
            landform = landform_data[landform_id]

            if pri_major < pri_secondary:
                key = tile.secondary
        else:
            landform = landform_data[key]

        tiles = tile_data['default'].copy()
        if landform['name'] in tile_data:
            tiles.update(tile_data[landform['name']])


        tile_key = key
        if len(tile.kinds) == 2 and not tile.full:
            # 两种地块和海相接
            if key == tile.major:
                tile_index = tile.value(key=tile.major) + 16 * tile.value(key=tile.secondary)
            else:
                tile_index = tile.value(key=tile.secondary) + 16 * tile.value(key=tile.major)
        else:
            tile_index = tile.value(key=tile_key)

        if tile_index not in tiles:
            tile_index = 0

        tile_meta_data = self.random.weight_choice(
            tiles[tile_index],
            value=lambda x: x,
            weight=lambda x: x.get('weight', 1)
        )


        tile_model_data = {
            'gim': landform['gim'] % tile_meta_data['gim'],
            'rotation': tile_meta_data.get('rotation', {'x': 0, 'y': 0, 'z': 0}),
            'scale': tile_meta_data.get('scale', {'x': 1, 'y': 1, 'z': 1}),
        }

        return tile_model_data

    def create_spot(self, grid, data):
        spots = []
        block_data = data['block']

        for block in block_data:
            if 'spots' not in block:
                continue
            amount = block['spots']['amount']
            task = grid.tiles(block['landform']['id'])
            while task:
                tile = task.pop()

                if not self.random.random_pass(amount):
                    continue

                # 概率检查
                spot = self.random.weight_choice(
                    block['spots']['spot'],
                    weight=lambda x: x['weight'],
                    value=lambda x: x['spot']
                )
                width = spot['horizontal']
                length = spot['vertical']

                # 随机方向
                y_rotation = self.random.choice([0, 90, 180, 270])
                if y_rotation == 90 or y_rotation == 270:
                    width, length = length, width

                # 检查区域是否可替换
                if not grid.validate_chunk(
                        tile.horizontal, tile.vertical,
                        tile.horizontal + width - 1, tile.vertical + length - 1,
                        block['landform']['id']
                ):
                    continue

                grid.remove_chunk(tile.horizontal, tile.vertical,
                                       tile.horizontal + width - 1, tile.vertical + length - 1)

                # 替换成装饰地块
                spots.append([
                    {
                        'comp': 'renderer',
                        'gim': spot['gim']
                    },
                    {
                        'comp': 'transform',
                        'position': {
                            'x': (tile.horizontal + width / 2.0 - 0.5) * data['world']['tile']['width'],
                            'y': -8,
                            'z': (tile.vertical + length / 2.0 - 0.5) * data['world']['tile']['length'],
                        },
                        'rotation': {
                            'y': y_rotation
                        }
                    }
                ])

        return spots

    def create_terrain(self, tiles, data):
        terrains = []
        for tile in tiles:
            tile_model_data = self.create_tile(tile, data['tile'], data['landform'])
            terrains.append([
                {
                    'comp': 'transform',
                    'position': {
                        'x': tile.horizontal * data['world']['tile']['width'],
                        'y': data['world']['layers']['terrain']['altitude'],
                        'z': tile.vertical * data['world']['tile']['length']
                    },
                    'rotation': tile_model_data['rotation'],
                    'scale': tile_model_data['scale']
                },
                {
                    'comp': 'renderer',
                    'gim': tile_model_data['gim']
                }
            ])
        return terrains

    def create_biosphere(self, region, data):
        '''
        创建生物群落组
        :param region: 可创建的区域
        :param data: 所有数据
        '''
        biosphere = []
        biosphere_created = []

        for block in data['block']:
            for biome in block['biomes']:
                amount = int(biome['amount'] * block['area'])
                nodes = region.get_nodes(block['landform']['id'])
                while amount > 0 and nodes:
                    # 随机选择源点
                    origin_index = self.random.randint(0, len(nodes) - 1)
                    origin = nodes.pop(origin_index)
                    cluster, amount = self.create_cluster(region, block, biosphere_created, origin, biome, data, amount)
                    biosphere.extend(cluster)
        return biosphere

    def create_cluster(self, region, block, biosphere_created, origin, biome_data, data, amount):
        '''
        地图上随机创建种群
        :param region: 创建的区域
        :param block: 地块
        :param biosphere_created: 已创建生物
        :param origin: 创建的源点
        :param biome_data: 生物数据
        :param data: 所有数据
        :param amount: 创建的总数
        :return: 剩余未创建的数量
        '''
        def check_biont_range(new_biont, biosphere_created):
            for biont_created in biosphere_created:
                dist = (biont_created['range'] + new_biont['range'])
                if Vector3.distance(biont_created['position'], new_biont['position']) < dist:
                    return False
            return True

        cluster = []
        cluster_amount = self.random.randint(*data['world']['biomes']['cluster'])
        for _ in xrange(cluster_amount):
            biome_range = biome_data['item']['creator']['range']
            size = data['world']['tile']['width'] * data['world']['tile']['length']

            amount -= 1
            if amount <= 0:
                break

            h = origin.horizontal + self.random.uniform(-0.5, 0.5) + self.random.gauss(0, 1.0 / biome_data['density'])
            v = origin.vertical + self.random.uniform(-0.5, 0.5) + self.random.gauss(0, 1.0 / biome_data['density'])

            padding = biome_range ** 2 / size

            if not region.inside(round(h), round(v), padding + 1, block['landform']['id']):
                continue

            position = Vector3(
                h * data['world']['tile']['width'],
                data['world']['layers']['biont']['altitude'],
                v * data['world']['tile']['length']
            )

            biont = {
                'position': position,
                'range': biome_range
            }

            # 是否和已有生物叠加
            if not check_biont_range(biont, biosphere_created):
                continue

            biosphere_created.append(biont)

            comps_data = [{
                'comp': 'transform',
                'position': {
                    'x': h * data['world']['tile']['width'],
                    'y': data['world']['layers']['biont']['altitude'],
                    'z': v * data['world']['tile']['length']
                },
                'rotation': {
                    'y': self.random.uniform(*data['world']['biomes']['rotation'])
                }
            }] + biome_data['item']['components']

            # 增加影子
            for idx, comp_data in enumerate(comps_data):
                if comp_data['comp'] == 'shadow':
                    comp_data = comp_data.copy()
                    if comp_data.get('gim') is None:
                        comp_data['gim'] = data['world']['shadow']['gim']
                    comp_data['block'] = str(block['name'])
                    comps_data[idx] = comp_data
            cluster.append(comps_data)

        return cluster, amount

    def create_building(self, grid, data):
        building_h = data['world']['building']['horizontal']
        building_v = data['world']['building']['vertical']
        margin = data['world']['building']['margin']
        def create_part(horizontal, vertical, side):
            offsets = [
                (0, building_v),
                (building_h, building_v),
                (0, 0), (building_h, 0)
            ]
            h = horizontal + offsets[side][0]
            v = vertical + offsets[side][1]

            # 检查区域是否可替换
            if not grid.validate_chunk(
                    h, v,
                    h + building_h - 1,
                    v + building_v - 1,
                    block['landform']['id']):
                return

            part_renderer = self.random.weight_choice(data['building'][side],
                                                             value=lambda x: x['part'], weight=lambda x: x['weight'])

            # 空地块
            if not part_renderer:
                return

            # 移除地块
            grid.remove_chunk(h, v, h + building_h - 1, v + building_v - 1)

            part_transform = [{
                'comp': 'transform',
                'position': {
                    'x': (h + building_h / 2 - 0.5) * data['world']['tile']['width'],
                    'y': -8,
                    'z': (v + building_v / 2 - 0.5) * data['world']['tile']['length'],
                }
            }]
            return part_renderer + part_transform

        buildings = []
        block_data = data['block']

        for block in block_data:
            if 'buildings' not in block:
                continue

            amount = block['buildings']['amount']

            task = grid.tiles(block['landform']['id'])
            while task:
                tile = task.pop()

                if not self.random.random_pass(amount):
                    continue

                if not grid.validate_chunk(
                        tile.horizontal - margin, tile.vertical - margin,
                        tile.horizontal + building_h * 2+ margin - 1,
                        tile.vertical + building_v * 2 + margin - 1, block['landform']['id']):
                    continue

                for side in xrange(0, 4):
                    part = create_part(tile.horizontal, tile.vertical, side)
                    if part:
                        buildings.append(part)

        return buildings

    # ============ Monster ============
    def get_component(self, data, comp_name):
        for comp in data:
            if comp['comp'] == comp_name:
                return comp.copy()

    def create_transition(self, data):
        from universe.manager import Transition
        return Transition(
            source=data['src'],
            destination=data['dst'],
            condition=data['condition']
        )

    def create_animator(self, data):
        from universe.manager import Animator
        transitions = []
        for tran_data in data.get('transitions', []):
            transitions.append(self.create_transition(tran_data))

        return Animator(
            default=data['default'],
            transitions=transitions
        )

    def create_collider(self, data):
        from universe.misc import Vector3, AABB
        if data['type'] == 'AABB':
            # AABB碰撞盒
            min_x = data['center']['x'] - data['shape']['width'] / 2.0
            min_y = data['center']['y'] - data['shape']['height'] / 2.0
            min_z = data['center']['z'] - data['shape']['length'] / 2.0
            max_x = data['center']['x'] + data['shape']['width'] / 2.0
            max_y = data['center']['y'] + data['shape']['height'] / 2.0
            max_z = data['center']['z'] + data['shape']['length'] / 2.0
            min_point = Vector3(min_x, min_y, min_z)
            max_point = Vector3(max_x, max_y, max_z)
            aabb = AABB(min_point, max_point)
            return aabb

    # ============ ECS components ============
    def create_colliders_comp(self, data):
        if data['comp'] != 'collider':
            raise TypeError
        from universe.component import Collider
        colliders = []
        for collider_data in data.get('colliders', []):
            collider = self.create_collider(collider_data)
            colliders.append(collider)
        return Collider(colliders=colliders, outline_visible=data.get('outline_visible', False))

    def create_transform_comp(self, data):
        if data['comp'] != 'transform':
            raise TypeError
        from universe.component import Transform
        from universe.misc import Vector3

        position_data = data.get('position', {})
        position = Vector3(
            position_data.get('x', 0),
            position_data.get('y', 0),
            position_data.get('z', 0),
        )

        rotation_data = data.get('rotation', {})
        rotation = Vector3(
            rotation_data.get('x', 0),
            rotation_data.get('y', 0),
            rotation_data.get('z', 0),
        )

        scale_data = data.get('scale', {})
        scale = Vector3(
            scale_data.get('x', 1),
            scale_data.get('y', 1),
            scale_data.get('z', 1),
        )
        return Transform(position, rotation, scale, static=data.get('static', True))

    def create_renderer_comp(self, data):
        if data['comp'] != 'renderer':
            raise TypeError
        from universe.component import Renderer
        scale_data = data.get('scale', {})
        scale = Vector3(
            scale_data.get('x', 1),
            scale_data.get('y', 1),
            scale_data.get('z', 1),
        )
        animator = None
        if 'animator' in data:
            animator = self.create_animator(data['animator'])
        return Renderer(
            gim=data['gim'],
            scale=scale,
            animator=animator
        )

    def create_shadow_comp(self, data):
        if data['comp'] != 'shadow':
            raise TypeError
        from universe.component import Shadow
        gim = data.get('gim')
        block = data.get('block')
        scale_data = data.get('scale', {})
        scale = Vector3(
            scale_data.get('x', 1),
            scale_data.get('y', 1),
            scale_data.get('z', 1),
        )
        return Shadow(
            gim=gim,
            block=block,
            scale=scale
        )

    def create_item_comp(self, data):
        if data['comp'] != 'item':
            raise TypeError
        from universe.component import Item
        return Item(
            id=data.get('id'),
            kind=data.get('kind'),
            name=data.get('name'),
            health=data.get('health'),
            reaped=data.get('reaped'),
            good=data.get('good')
        )

    def create_monster_comp(self, data):
        if data['comp'] != 'monster':
            raise TypeError
        from universe.component import Monster
        return Monster(
            move_speed=data['move_speed'],
            attack_speed=data['attack_speed'],
            attack_range=data['attack_range'],
            detection_range=data['detection_range']
        )

    def create_player_comp(self, data):
        if data['comp'] != 'player':
            raise TypeError
        from universe.component import Player
        return Player()

    def create_components(self, data):
        comps = []
        for comp_data in data:
            if comp_data['comp'] == 'collider':
                comps.append(self.create_colliders_comp(comp_data))
            elif comp_data['comp'] == 'transform':
                comps.append(self.create_transform_comp(comp_data))
            elif comp_data['comp'] == 'renderer':
                comps.append(self.create_renderer_comp(comp_data))
            elif comp_data['comp'] == 'shadow':
                comps.append(self.create_shadow_comp(comp_data))
            elif comp_data['comp'] == 'item':
                comps.append(self.create_item_comp(comp_data))
            elif comp_data['comp'] == 'monster':
                comps.append(self.create_monster_comp(comp_data))
            elif comp_data['comp'] == 'player':
                comps.append(self.create_player_comp(comp_data))
        return comps

