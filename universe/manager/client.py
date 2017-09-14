# coding=utf-8
try:
    import game3d
    game3d.load_plugin("world.dll")
    import world
    import math3d
    import render
except ImportError:
    world = None
    math3d = None
    render = None


class Client(object):
    def __init__(self):
        self.scene = None
        self.scene_manager = None
        self.main_camera = None

        self.nexo_world = world
        self.nexo_math3d = math3d
        self.nexo_render = render

        self.loaded = False
        self.loaded_models = 0
        self.total_models = 0
        self.loading_panel = None

        self.universe = None
        self.grid = None

        self.step = 0
        self.last_outline_model = None
        self.last_shelter_model = None

    @property
    def is_client(self):
        return self.scene_manager is not None

    def clear(self):
        self.loaded = False
        self.loaded_models = 0
        self.total_models = 0

    def set_loading_progress(self, percentage):
        self.loading_panel.set_percentage(percentage)

    def on_loading_finished(self):
        if not self.loaded:
            if self.scene_manager:
                self.loaded = True
                self.scene_manager.send_load_map_finished_msg()

    def start_game(self):
        from ui.PanelFight import PanelFight
        PanelFight(self.scene_manager).show(True)
        self.enable_outline()

    def enable_outline(self):
        render.set_post_process_active('smooth_outline', True)
        mat = render.get_post_process_material('smooth_outline', 0)
        mat.set_var('width', 1.0)
        mat = render.get_post_process_material('smooth_outline', 1)
        mat.set_var('width', 1.0)
        mat = render.get_post_process_material('smooth_outline', 2)
        mat.set_var('brightness', 2.0)

    def set_loaded_models(self, val):
        if self.loaded:
            return
        self.loaded_models = val
        if self.total_models <= 0:
            self.on_loading_finished()
            return
        percentage = val * 100.0 / self.total_models
        percentage = max(min(percentage, 100), 1)
        self.set_loading_progress(percentage)
        if percentage >= 100:
            self.on_loading_finished()

    def outline(self, model, enable=True):
        if model:
            try:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, enable)
                model.set_ext_technique_var(render.EXT_TECH_SMOOTH_OUTLINE, "OutlineColor", (1.0, 1.0, 0.0, 1.0))
            except:
                pass

    def create_grid_line(self, grid_width, grid_length, cell_width, cell_length):
        y = 5
        c = 0xFFFFFFFF
        grid = []
        for column in xrange(0, grid_width + 1):
            x = (column - grid_width / 2) * cell_width
            z = grid_length / 2 * cell_length
            grid.append(((x, y, -z), (x, y, z), c))

        for row in xrange(0, grid_length + 1):
            z = (row - grid_length / 2) * cell_length
            x = grid_width / 2 * cell_width
            grid.append(((-x, y, z), (x, y, z), c))

        return grid

    def set_grid_visible(self, visible):
        if visible:
            if self.grid is None:
                grid_vertices = self.create_grid_line(200, 200, 800, 800)
                prim = self.nexo_world.primitives(self.scene)
                prim.create_line(grid_vertices)
                self.grid = prim
        else:
            if self.grid:
                self.grid.destroy()
                self.grid = None

    def step_load(self, dst, step=2.0):
        '''
        分步加载
        :return:
        '''
        while self.step < dst:
            self.step += step
            yield self.step

    def step_create(self):
        '''
        分帧创世
        '''
        # 层管理
        from universe.manager import Layer
        self.universe.layer = Layer(self.universe, data=self.universe.data['world']['layers'])

        # 创建虚拟玩家
        self.universe.create_player()

        for step in self.step_load(10):
            yield step

        # 创建区域
        self.universe.region = self.universe.creator.create_region(self.universe.data)
        grid = self.universe.region.grid()

        for step in self.step_load(20):
            yield step

        # 创建建筑
        buildings = self.universe.creator.create_building(grid, self.universe.data)
        self.universe.create_entities('terrain', buildings)

        for step in self.step_load(30):
            yield step

        # 地图污点装饰
        spots = self.universe.creator.create_spot(grid, self.universe.data)
        self.universe.create_entities('terrain', spots)

        for step in self.step_load(50):
            yield step

        # 创建地形
        terrains = self.universe.creator.create_terrain(grid.tiles(), self.universe.data)
        self.universe.create_entities('terrain', terrains)

        for step in self.step_load(70):
            yield step

        # 创造环境生物
        biosphere = self.universe.creator.create_biosphere(self.universe.region, self.universe.data)
        self.universe.create_entities('biont', biosphere)

        for step in self.step_load(90):
            yield step

        # 创建怪物
        # self.create_monster_entity()

        # 创建处理器
        self.universe.create_processor()

        # 初始化
        self.universe.world.start()

        for step in self.step_load(100, 1.0):
            yield step


    def shelter_transparency(self):
        '''
        遮挡透明
        :return:
        '''
        from universe.misc import Vector3, Ray
        from universe.component import Transform, Renderer, Collider
        transform = self.universe.world.component_for_entity(self.universe.player['entity'], Transform)

        ray_origin = transform.position + Vector3(0, 200, 0)
        ray_direction = Vector3().copy(self.scene.active_camera.position) - transform.position
        ray = Ray(ray_origin, ray_direction)

        # last_shelter_model
        for ent, (rend, coll) in self.universe.world.get_components(Renderer, Collider):
            if coll.intersect(ray):
                # rend.model.enable_instancing(False)
                # rend.model.all_materials.transparent_mode = self.nexo_render.TRANSPARENT_MODE_ALPHA_R_Z
                # rend.model.alpha = 100
                pass
            else:
                # rend.model.enable_instancing(True)
                # rend.model.all_materials.transparent_mode = self.nexo_render.TRANSPARENT_MODE_UNSET
                # rend.model.alpha = 255
                pass

    def highlight_near_item(self, origin, radius=200):
        '''
        高亮附近可采集物体
        :return:
        '''
        entity, model, _ = self.universe.get_target_entity(origin, radius)

        if model != self.last_outline_model:
            self.outline(self.last_outline_model, False)
            self.last_outline_model = None
        if model:
            self.last_outline_model = model
            self.outline(model, True)

_inst = Client()

def ClientOnly(func):
    def _deco(*args, **kwargs):
        if _inst.nexo_world:
            return func(*args, **kwargs)
        else:
            return None
    return _deco