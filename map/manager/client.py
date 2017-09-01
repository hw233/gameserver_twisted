
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
        self.universe = None
        self.world = world
        self.math3d = math3d
        self.render = render


_inst = Client()
scene = _inst.scene
universe = _inst.universe
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