# coding=utf-8
import math
from MapGrid import MapBound
from MapData import MapData
from MapRule import AreaRule
from MapItem import MapItem
from MapMath import GridPosition
from MapLayer import MapLayerManager, MapLayer
import MapUtil

class MapBlock(MapData):
    def __init__(self, map_world, data, grid):
        self.map_world = map_world
        self.data = data
        self.grid = grid
        self.bound = MapBound()
        self.inner_cells = []     # 内部地块
        self.outline_cells = []   # 边缘地块
        self.init_layer()   # 初始化层管理器

    def init_layer(self):
        self.layer_manager = MapLayerManager()
        self.layer_manager.add_layer(MapLayer("terrain", 0))
        self.layer_manager.add_layer(MapLayer("spot", 4))
        self.layer_manager.add_layer(MapLayer("biome", 6))

    def add_inner_cell(self, cell):
        '''
        增加内部地块
        :param position: 网格坐标
        :param deep: 距离边缘的深度
        :return:
        '''
        self.inner_cells.append(cell)

    def add_outline_cell(self, cell):
        self.outline_cells.append(cell)

    @property
    def layers(self):
        return self.layer_manager.all

    def add_item(self, layer, item):
        self.layer_manager.get_layer(layer).add_item(item)

    def get_item(self, layer, item):
        if layer is None:
            for _layer in self.layer_manager.all:
                _item = _layer.get_item(item)
                if _item:
                    return _item
        else:
            return self.layer_manager.get_layer(layer).get_item(item)


    def get_items(self, layer=None):
        items = []
        if layer is None:
            for _layer in self.layer_manager.all:
                items.extend(_layer.items)
        else:
            items.extend(self.layer_manager.get_layer(layer).items)
        return items

    def remove_item(self, layer, item):
        if layer is None:
            for _layer in self.layer_manager.all:
                _layer.remove_item(item)
        else:
            self.layer_manager.get_layer(layer).remove_item(item)

    def create_spots(self):
        for spot_group in self.data["spots"]:
            amount = int(self.data["area"] * spot_group["proportion"])
            try_times = 100
            while amount > 0 and self.inner_cells:
                try_times -= 1
                if try_times <= 0:
                    break

                spot_data = MapUtil.random.choice(spot_group["spot"])
                inner_cell = MapUtil.random.choice(self.inner_cells)
                offset_row = MapUtil.random.uniform(0, 1)
                offset_column = MapUtil.random.uniform(0, 1)
                spot_position = inner_cell.position + GridPosition(offset_row, offset_column)
                spot = MapItem(self.map_world.generate_id(), spot_data, spot_position)
                if not self.place_check("spot", spot):
                    continue
                amount -= 1
                self.add_item("spot", spot)

    def in_block(self, item):
        '''
        是否在block的区域范围内
        :param bound:
        :param position:
        :return:
        '''
        for pos in item.bound.all:
            cell = self.grid.get_cell(pos)
            if cell not in self.inner_cells or not cell.corner.full:
                return False
        return True


    def place_check(self, layer, item):
        # 检测是否和已有相交
        for other in self.get_items(layer):
            if item.bound.intersect(other.bound):
                return False

        # 是否在地块内
        if not self.in_block(item):
            return False

        return True

    def create_biomes(self, data=None):
        '''
        创建生物群落组
        :param block:
        :param biome:
        '''
        if data is None:
            data = self.data["biomes"]

        for biome in data:
            amount = int(biome["proportion"] * self.data["area"])
            while amount > 0 and self.inner_cells:
                cell = MapUtil.random.choice(self.inner_cells)
                amount = self.create_biome(biome, cell.position, amount)
                # 伴生生物
                if "associated" in biome:
                    for as_biome in biome["associated"]:
                        as_amount = int(as_biome["proportion"] * self.data["area"])
                        self.create_biome(as_biome, cell.position, as_amount)


    def create_biome(self, data, center, amount):
        '''
        地图上随机创建群落
        :param center: 群落中心
        :param density: 密度 对应正态分布的标准差
        :param amount: 创建的总数
        :return: 剩余未创建的数量
        '''
        count = amount
        try_times = 100    # 最多尝试次数
        while count > 0:
            try_times -= 1
            if try_times <= 0:
                # 多次尝试失败则强制减1
                count -= 1
                break

            row = center.row + MapUtil.random.gauss(0, 1.0 / data["density"])
            column = center.column + MapUtil.random.gauss(0, 1.0 / data["density"])
            position = GridPosition(row, column)
            biome = MapItem(self.map_world.generate_id(), data["item"], position)
            # 是否可以放置物体
            if not self.place_check("biome", biome):
                continue

            self.add_item("biome", biome)
            count -= 1
            # 按照一定概率停止，已生成比重越重则停止的概率越大
            if MapUtil.random.uniform(0, 1) < (amount - count) * 1.0 / amount or amount - count > 2:
                break
        return count

    def create_terrain(self, tile_data):
        for cell in self.inner_cells + self.outline_cells:
            if cell.corner.empty:
                continue
            tile_index = MapUtil.weight_choice(
                tile_data[cell.corner.tile],
                lambda x: x[0],
                lambda x: x[1]
            )
            gim = self.data["landform"]["gim"] % (tile_index)
            data = {
                "gim": gim,
                "width": self.grid.cell_bound.width,
                "height": self.grid.cell_bound.height
            }
            terrain = MapItem(self.map_world.generate_id(), data, cell.position)
            self.add_item("terrain", terrain)

    def dig_holes(self):
        '''
        在地面上挖洞
        :return:
        '''
        target = self.data["holes"]["area"]
        start = MapUtil.random.choice(self.inner_cells)
        task = [start]
        self.grid.clear_cells(start.position)
        count = target
        while task and count > 0:
            current = task.pop()
            for offset in self.grid.NEIGHBORS_OFFSET:
                further_position = current.position + offset
                further = self.grid.get_cell(further_position)
                # 可访问性检查

                if further is None or further not in self.inner_cells + self.outline_cells:
                    continue

                if MapUtil.grow_divide(target - count, target):
                    further = MapUtil.random.choice(self.inner_cells)

                count -= 1
                if count <= 0:
                    break

                self.grid.clear_cells(further.position)
                task.append(further)

class MapBlockManager(object):
    def __init__(self, grid):
        self.grid = grid
        self.blocks = []

    @property
    def all(self):
        for block in self.blocks:
            yield block

    def add_block(self, block):
        self.blocks.append(block)

    def create_block(self, block):
        '''
         创建一片地块
         '''
        self.add_block(block)

        # 面积约束
        area_rule = AreaRule(block.data["area"])

        # 标记起始点
        center = block.data["center"].absolute_by(self.grid.bound.position)
        filled = self.grid.fill_cells(center, block.data["landform"]["id"])
        area_rule.increase(filled)
        block.bound.position = center
        block.bound.extend(center)

        task = [center]

        # 随机生成地块
        while task and area_rule.validated:
            rand_task = MapUtil.random.randint(0, len(task) - 1)
            current = task.pop(rand_task)
            for offset in self.grid.STRAIGHT_NEIGHBORS_OFFSET:
                # 可访问性检查
                further = current + offset
                cell = self.grid.get_cell(further)

                if cell is None or cell.corner.full:
                    continue

                # 形状限制
                # if not ShapeRule.like_circle(center, further, radius):
                #     continue

                # 设置地块
                filled = self.grid.fill_cells(further, block.data["landform"]["id"])

                area_rule.increase(filled)
                if not area_rule.validated:
                    break

                # 扩展区域
                block.bound.extend(further)
                task.append(further)

        # BFS访问标记
        visit = {}

        # 首先插入边缘地块
        for pos in block.bound.all:
            cell = self.grid.get_cell(pos)
            if cell is None or cell in visit:
                continue
            if block.data["landform"]["id"] in cell.corner.filled:
                if cell.corner.partial:
                    block.add_outline_cell(cell)
                    visit[cell] = True

        # BFS确认内部地块到边缘的深度
        task = []
        task.extend(block.outline_cells)
        while task:
            current = task.pop(0)
            for offset in self.grid.STRAIGHT_NEIGHBORS_OFFSET:
                position = current.position + offset
                further = self.grid.get_cell(position)
                if further is not None and further not in visit:
                    if block.data["landform"]["id"] in further.corner.filled:
                        visit[further] = True
                        block.add_inner_cell(further)
                        task.append(further)

        # 内部坑洞
        block.dig_holes()
