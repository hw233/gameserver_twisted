
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
        self.world = world
        self.math3d = math3d
        self.render = render
        self.loading_panel = None
        self.loaded = False
        self.loaded_models = 0
        self.total_models = 0
        self.panel_fight = None

    def show_loading(self):
        from ui.LoadingPanel import LoadingPanel
        self.loading_panel = LoadingPanel()
        self.loading_panel.show(True)

    def set_loading_progress(self, percentage):
        self.loading_panel.set_percentage(percentage)

    def on_loading_finished(self):
        if self.scene_manager:
            from ui.PanelFight import PanelFight
            self.panel_fight = PanelFight(self.scene_manager)
            self.panel_fight.show(True)

    def get_total_models(self):
        return self.total_models

    def set_total_models(self, val):
        self.total_models = val

    def get_loaded_models(self):
        return self.loaded_models

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
            self.loaded = True
            self.on_loading_finished()

    def get_scene_manager(self):
        return self.scene_manager

    def set_scene_manager(self, val):
        self.scene_manager = val

    def get_scene(self):
        return self.scene

    def set_scene(self, val):
        self.scene = val


_inst = Client()
get_loaded_models = _inst.get_loaded_models
set_loaded_models = _inst.set_loaded_models

set_total_models = _inst.set_total_models
get_total_models = _inst.get_total_models

get_scene_manager = _inst.get_scene_manager
set_scene_manager = _inst.set_scene_manager

show_loading = _inst.show_loading
set_loading_progress = _inst.set_loading_progress

get_scene = _inst.get_scene
set_scene = _inst.set_scene

nexo_world = _inst.world
nexo_math3d = _inst.math3d
nexo_render = _inst.render

def only(func):
    def _deco(*args, **kwargs):
        if _inst.world:
            return func(*args, **kwargs)
        else:
            return None
    return _deco