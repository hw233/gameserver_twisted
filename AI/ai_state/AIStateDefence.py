from common import conf
from state.StateBase import StateBase
from ui import CCUIManager

class StateDefence(StateBase):
    def __init__(self, name, entity, config):
        super(StateDefence, self).__init__(name, entity, config)

    def enter(self, data):
        change = self.config.get('change')
        if change is None:
            return

        self.entity.get_state(conf.STATE_IDLE).set_default_anim(change.get('idle'))
        self.entity.get_state(conf.STATE_MOVE).set_default_anim(change.get('run'))

        CCUIManager.get_ui_by_name("zhandoujiemian.defend").set_check_box_state(False)

    def exit(self):
        self.entity.get_state(conf.STATE_IDLE).clear_default_anim()
        self.entity.get_state(conf.STATE_MOVE).clear_default_anim()

        CCUIManager.get_ui_by_name("zhandoujiemian.defend").set_check_box_state(True)

    def get_speed_percentage(self):
        change = self.config.get('change')
        if change is None:
            return
        return change.get('speed_percentage', 1.0)
