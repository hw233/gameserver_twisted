# coding=utf-8
class Renderer(object):
    def __init__(self, gim=None, visible=True, alpha=1.0, primitive=None):
        self.gim = gim
        self.visible = visible
        self.alpha = alpha
        self.primitive = primitive
        self.model = None


class Animator(object):
    def __init__(self, default, states, parameters, transitions):
        self.state = default                # 当前状态
        self.states = states                # 所有状态
        self.parameters = parameters        # 参数
        self.transitions = transitions      # 转换

    def set_parameter(self, name, value):
        self.parameters[name]['value'] = value
