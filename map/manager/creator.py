# coding=utf-8

from map.misc import PseudoRandom, Vector3
from rule import AreaRule
import graph

class Creator(object):

    @staticmethod
    def create_block(region, origin, data):
        '''
        创建区域
        :return:
        '''
        # 面积约束
        area_rule = AreaRule(data['area'])
        origin.value = data['landform']['id']
        task = [origin]
        while task and area_rule.validated:
            current = PseudoRandom.get().choice(task)
            task.remove(current)

            # 邻边扩张
            for direction in graph.NEIGHBORS:
                further = current.neighbour(direction)
                further.value = data['landform']['id']
                if region.get_node(further.horizontal, further.vertical) is None:
                    region.add_node(further)
                    area_rule.increase()
                    if not area_rule.validated:
                        break
                    task.append(further)

    @staticmethod
    def create_region(data):
        region = graph.Region()
        for block_data in data:
            origin = graph.Node(
                horizontal=block_data['center'][0],
                vertical=block_data['center'][1]
            )
            Creator.create_block(region, origin, block_data)
        return region

    @staticmethod
    def create_tile(tile, tile_data, landform_data):
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

        tile_meta_data = PseudoRandom.get().weight_choice(
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

    @staticmethod
    def create_spot(grid, data):
        spots = []
        block_data = data['block']

        for block in block_data:
            if 'spots' not in block:
                continue

            block_tiles = filter(lambda x: x.full and x.major == block['landform']['id'], grid.tiles)

            sum = 0
            for x in grid.tiles:
                sum += x.value()

            if not block_tiles:
                continue

            area = block['spots']['area'] * block['area']
            while area > 0:
                tile = PseudoRandom.get().choice(block_tiles)
                spot = PseudoRandom.get().choice(block['spots']['spot'])
                width = spot['horizontal']
                length = spot['vertical']

                # 随机方向
                y_rotation = PseudoRandom.get().choice([0, 90, 180, 270])
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

                area -= width * length

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

    @staticmethod
    def create_terrain(tiles, data):
        terrains = []
        for tile in tiles:
            tile_model_data = Creator.create_tile(tile, data['tile'], data['landform'])
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

    @staticmethod
    def create_biosphere(region, data):
        '''
        创建生物群落组
        :param region: 可创建的区域
        :param data: 所有数据
        '''
        biosphere = []
        biosphere_created = []

        for block in data['block']:
            for biome in block['biomes']:
                amount = int(biome['proportion'] * block['area'])
                nodes = region.get_nodes(block['landform']['id'])
                while amount > 0 and region and nodes:
                    origin = PseudoRandom.get().choice(nodes)
                    population, amount = Creator.create_population(region, biosphere_created, origin, biome, data, amount)
                    biosphere.extend(population)
                    # 伴生生物
                    if 'associated' in biome:
                        for as_biome in biome['associated']:
                            as_amount = int(as_biome['proportion'] * block['area'])
                            as_population, as_amount = Creator.create_population(region, biosphere_created, origin, as_biome, data, as_amount)
                            biosphere.extend(as_population)
        return biosphere

    @staticmethod
    def create_population(region, biosphere_created, origin, biome_data, data, amount):
        '''
        地图上随机创建种群
        :param region: 创建的区域
        :param biosphere_created: 已创建生物
        :param origin: 创建的源点
        :param biome_data: 生物数据
        :param data: 所有数据
        :param amount: 创建的总数
        :return: 剩余未创建的数量
        '''

        def check_biont_range(new_biont, biosphere_created):
            for biont_created in biosphere_created:
                min_dis = (biont_created['range'] + new_biont['range'])
                if Vector3.distance(biont_created['position'], new_biont['position']) < min_dis:
                    return False
            return True


        population = []
        count = amount
        try_times = 5000    # 最多尝试次数
        while count > 0:
            try_times -= 1
            if try_times <= 0:
                # 多次尝试失败则强制减1
                count -= 1
                break

            h = origin.horizontal + PseudoRandom.get().gauss(0, 1.0 / biome_data['density'])
            v = origin.vertical + PseudoRandom.get().gauss(0, 1.0 / biome_data['density'])

            biome_range = biome_data['item']['creator']['range']
            padding = biome_range / max(data['world']['tile']['width'],
                                        data['world']['tile']['length'])
            if not region.inside(h, v, padding + 1):
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
                }
            }] + biome_data['item']['components']

            population.append(comps_data)

            count -= 1
            # 按照一定概率停止，已生成比重越重则停止的概率越大
            if PseudoRandom.get().uniform(0, 1) < (amount - count) * 1.0 / amount or amount - count > 2:
                break
        return population, count

    @staticmethod
    def create_building(grid, data):
        building_h = data['world']['building']['horizontal']
        building_v = data['world']['building']['vertical']
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

            # 移除地块
            grid.remove_chunk(h, v, h + building_h - 1, v + building_v - 1)
            part_renderer = PseudoRandom.get().choice(data['building'][side])

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

            block_tiles = filter(lambda x: x.full and x.major == block['landform']['id'], grid.tiles)

            area = block['buildings']['area'] * block['area']

            try_times = 1000
            while area > 0:
                try_times -= 1
                if try_times <=0 :
                    break

                tile = PseudoRandom.get().choice(block_tiles)

                for side in xrange(0, 4):
                    part = create_part(tile.horizontal, tile.vertical, side)
                    if part:
                        buildings.append(part)
                        area -= 1
        return buildings

    @staticmethod
    def create_collider(data):
        if data['comp'] != 'collider':
            raise TypeError
        if data['type'] == 'AABB':
            # AABB碰撞盒
            from map.component import Collider
            from map.misc import Vector3, AABB
            min_x = data['center']['x'] - data['shape']['width'] / 2.0
            min_y = data['center']['y'] - data['shape']['height'] / 2.0
            min_z = data['center']['z'] - data['shape']['length'] / 2.0
            max_x = data['center']['x'] + data['shape']['width'] / 2.0
            max_y = data['center']['y'] + data['shape']['height'] / 2.0
            max_z = data['center']['z'] + data['shape']['length'] / 2.0
            min_point = Vector3(min_x, min_y, min_z)
            max_point = Vector3(max_x, max_y, max_z)
            aabb = AABB(min_point, max_point)
            return Collider(aabb, outline_visible=data.get('outline_visible', False))

    @staticmethod
    def create_transform(data):
        if data['comp'] != 'transform':
            raise TypeError
        from map.component import Transform
        from map.misc import Vector3

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
        return Transform(position, rotation, scale)

    @staticmethod
    def create_renderer(data):
        if data['comp'] != 'renderer':
            raise TypeError
        from map.component import Renderer
        return Renderer(gim=data['gim'])

    @staticmethod
    def create_animator(data):
        if data['comp'] != 'animator':
            raise TypeError
        from map.component import Animator
        # print data
        # return Animator(
        #     default=
        # )

    @staticmethod
    def create_item(data):
        if data['comp'] != 'item':
            raise TypeError
        from map.component import Item
        return Item(
            id=data.get('id'),
            kind=data.get('kind'),
            name=data.get('name'),
            health=data.get('health'),
            reaped=data.get('reaped'),
            drop_good=data.get('drop_good'),
            good_id=data.get('good_id')
        )

    @staticmethod
    def create_components(data):
        comps = []
        for comp_data in data:
            if comp_data['comp'] == 'collider':
                comps.append(Creator.create_collider(comp_data))
            elif comp_data['comp'] == 'transform':
                comps.append(Creator.create_transform(comp_data))
            elif comp_data['comp'] == 'renderer':
                comps.append(Creator.create_renderer(comp_data))
            # elif comp_data['comp'] == 'animator':
            #     Creator.create_animator(comp_data)
            elif comp_data['comp'] == 'item':
                comps.append(Creator.create_item(comp_data))
        return comps

