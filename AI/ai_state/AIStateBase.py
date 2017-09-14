# coding=utf-8


class StateBase(object):
    def __init__(self, name, entity, config):
        super(StateBase, self).__init__()
        self.entity = entity
        self.name = name
        self.id = config.get('id')
        self.config = config
        self.default_anim = None

    def execute(self):
        pass

    def enter(self, data):
        pass

    def exit(self):
        pass

    def get_name(self):
        return self.name

    def can_enter_state(self, name):
        """
        是否可以从当前状态进入name状态
        :param name: 状态名
        """
        if self.config.get(name, 0) == 1:
            return False
        return True

    def get_anim_name(self, ani_map='ani'):
        ani_name = self.default_anim
        if ani_name is not None:
            return ani_name
        wid = self.entity.weapon_handler.get_current_weapon_id()
        ani_conf = self.config.get(ani_map)
        if wid is not None:
            ani_name = ani_conf.get(str(wid))
        if ani_name is None:
            ani_name = ani_conf.get('all')
        return ani_name

    def is_collider_work(self):
        if self.config.get('block') == 1:
            return False
        return True

    def set_default_anim(self, anim):
        self.default_anim = anim

    def clear_default_anim(self):
        self.default_anim = None

    def del_myself(self, state_name):
        if self.config.get(state_name) == 2:
            return True
        return False
