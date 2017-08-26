# -*- coding:utf-8 -*-

import MapUtil
from MapBlock import MapBlock, MapBlockManager
from MapLayer import MapLayerManager, MapLayer
from MapGrid import Grid
from MapMath import GridPosition, Vector3
from MapData import MapData
from MapItem import MapItem


# 地图生成
class MapWorld(MapData):
    grid = None

    def __init__(self, client=None):
        self.data = None
        self.models = []
        self.client = client
        self.id_count = -1
        if self.client:
            self.client.set_map_world(self)

    def generate_id(self):
        self.id_count += 1
        return self.id_count

    def init_layer(self):
        self.layer_manager = MapLayerManager()
        self.layer_manager.add_layer(MapLayer("ocean", self.data["water"]["altitude"]))

    def add_water_model(self):
        '''
        创建水面
        '''
        water = MapItem(self.generate_id(), self.data["water"], GridPosition(0, 0))
        self.layer_manager.get_layer("ocean").add_item(water)

    def create_world(self, seed=None):
        '''
        创建世界
        :return:
        '''
        # 设置伪随机种子
        MapUtil.random.seed(seed)

        self.data = MapData.load('world')
        self.init_layer()
        self.grid = Grid(
            width=self.data["grid"]["width"],
            height=self.data["grid"]["height"],
            cell_width=self.data["cell"]["width"],
            cell_height=self.data["cell"]["height"],
        )
        self.grid.set_block_manager(MapBlockManager(self.grid))

        blocks_data = MapData.load('block')
        for block_data in blocks_data:
            block = MapBlock(self, block_data, self.grid)
            # 创建区域
            self.grid.block_manager.create_block(block)
            # 创建地面
            block.create_terrain(tile_data=MapData.load('tile'))
            # 创建污点地块
            block.create_spots()
            # 创建生物群落
            block.create_biomes()
        # 增加水面
        self.add_water_model()

        # 实例化所有模型
        if self.client:
            self.client.instantiate_models()

        # 生成id
        self.generate_id()

        for block in self.grid.block_manager.all:
            print [i.id for i in block.get_items("biome")]

    def approach(self, src_pos, dst_pos):
        '''
        是否可以从当前位置移动到目标位置
        :param src_pos: 当前位置math3d.vector
        :param dst_pos: 目标位置math3d.vector
        :return:
        '''
        y = dst_pos.y

        if self.client:
            self.client.blend_model(Vector3(dst_pos.x, y, dst_pos.z))

        src_pos = self.grid.vector_to_grid(src_pos.x, src_pos.z)
        dst_pos = self.grid.vector_to_grid(dst_pos.x, dst_pos.z)

        # TODO current target不在同一个cell时候应该进行寻路
        current_cell = self.grid.get_cell(src_pos)
        target_cell = self.grid.get_cell(dst_pos)

        if target_cell.walkable(dst_pos):
            # 目标点两个轴向都可行则直接通过
            x, z = self.grid.grid_to_vector(dst_pos)
            return Vector3(x, y, z)

        # 如果目标点不可行，则判断两个轴向的分量
        x_walkable = target_cell.walkable(GridPosition(src_pos.row, dst_pos.column))
        z_walkable = target_cell.walkable(GridPosition(dst_pos.row, src_pos.column))

        # 修正后的目标位置
        guide = GridPosition()

        guide.column = dst_pos.column if x_walkable else src_pos.column
        guide.row = dst_pos.row if z_walkable else src_pos.row

        x, z = self.grid.grid_to_vector(guide)

        return Vector3(x, y, z)

    def get_item(self, id):
        for block in self.grid.block_manager.all:
            item = block.get_item('biome', id)
            if item:
                return item

    def remove_item(self, item):
        for block in self.grid.block_manager.all:
            block.remove_item('biome', item)

    def get_nearest_item(self, x, y, z):
        '''
        获取最近的物件
        :param x, y, z: 玩家位置
        :return:
        '''
        # TODO 使用BVH优化
        collect_range = 1

        min_dist = float("inf")
        nearest_item = None
        position = self.grid.vector_to_grid(x, z)
        for block in self.grid.block_manager.all:
            for item in block.get_items("biome"):
                dist = item.bound.position.distance_to(position)
                if dist < min_dist:
                    min_dist = dist
                    nearest_item = item

        if min_dist < collect_range:
            return nearest_item
        else:
            return None


    def client_reap(self, id):
        '''
        客户端打击表现
        :param id:
        :return:
        '''
        item = self.get_item(id)
        if item and item.hittable:
            self.client.play_animation(item, 'hit')

    def server_reap(self, id):
        '''
        服务端打击计算
        :param id: 编号
        :return 是否死亡
        '''
        item = self.get_item(id)
        if item and item.hittable:
            item.take_damage()
            return item.dead
        return False

    def client_drop(self, item_from):
        '''
        掉落物体
        :return:
        '''
        pass

    def server_drop(self, item_from):
        pass

    def client_destroy(self, id):
        '''
        摧毁物体
        :param id:
        :return:
        '''
        item = self.get_item(id)
        if item:
            item.model.play_animation('fall')
            # self.client.destroy_model(item.model)
            item.model = None
            self.remove_item(item)
            dead_data = item.data.get('dead')
            if dead_data:
                dead_item = MapItem(self.generate_id(), dead_data, item.bound.position)
                self.client.instantiate_model(dead_item)

    def server_destroy(self, id):
        '''
        摧毁物体
        :param id:
        :return:
        '''
        item = self.get_item(id)
        if item:
            self.remove_item(item)
            # 生成遗留物品
            dead_data = item.data.get('dead')
            if dead_data:
                dead_item = MapItem(self.generate_id(), dead_data, item.bound.position)
                # 添加到列表 TODO

    def client_collect(self, id):
        '''
        客户端捡起表现
        :param id:
        :return:
        '''
        item = self.get_item(id)
        if item and item.collectible:
            if self.client:
                self.client.destroy_model(item.model)
                item.model = None
            self.remove_item(item)

    def server_collect(self, id):
        '''
        服务端捡起计算
        :param id:
        :return:
        '''
        item = self.get_item(id)
        if item and item.collectible:
            self.remove_item(item)
