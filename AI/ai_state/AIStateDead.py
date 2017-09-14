from state.StateBase import StateBase


class StateDead(StateBase):
    def __init__(self, name, entity, config):
        super(StateDead, self).__init__(name, entity, config)

    def enter(self, data):
        ani_name = self.get_anim_name()
        self.entity.play_animation(ani_name)
