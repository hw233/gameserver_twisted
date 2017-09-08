# coding=utf-8
from common import conf

NAME_TO_CLASS = {
    conf.STATE_IDLE: 'StateIdle',
    conf.STATE_MOVE: 'StateMove',
    conf.STATE_ATTACK: 'StateAttack',
    conf.STATE_STIFFNESS: 'StateStiffness',
    conf.STATE_DEAD: 'StateDead',
    conf.STATE_LIEDOWN: 'StateLieDown',
    conf.STATE_HOLD_FORCE: 'StateHoldForce',
    conf.STATE_DEFENCE: 'StateDefence',
    conf.STATE_HOLD_FORCE_SINGLE: 'StateHoldForceSingle',
}


class StateMachine(object):
    def __init__(self, entity, config_file_name):
        super(StateMachine, self).__init__()
        self.entity = entity
        self.state_map = {}
        self.cur_state = None  # 父状态，只能有一个
        self.cur_sub_states = {}  # 子状态，可以有多个
        self.setup(config_file_name)
        self.change_state(conf.STATE_IDLE)

    def update(self):
        if self.cur_state:
            self.cur_state.execute()
        for state in self.cur_sub_states.itervalues():
            state.execute()

    def add_sub_state(self, state_name, data):
        state = self.state_map[state_name]
        self.cur_sub_states[state_name] = state
        state.enter(data)

    def del_sub_state(self, state_name):
        if state_name in self.cur_sub_states:
            self.cur_sub_states[state_name].exit()
            del self.cur_sub_states[state_name]

    def get_sub_state(self, state_name):
        return self.cur_sub_states.get(state_name)

    def get_state(self, state_name):
        return self.state_map.get(state_name)

    def change_state(self, state_name, data=None):
        """
        转换状态
        """
        if self.cur_state:
            self.cur_state.exit()
        self.cur_state = self.state_map.get(state_name)
        if self.cur_state is not None:
            self.cur_state.enter(data)
            # delete sub states
            del_names = []
            for name, state in self.cur_sub_states.iteritems():
                if state.del_myself(state_name):
                    del_names.append(name)
            for name in del_names:
                self.del_sub_state(name)

    def setup(self, config_file_name):
        """
        为每个状态创造一个类
        """
        config = __import__(config_file_name, fromlist=['']).data
        for name, info in config.iteritems():
            if name not in NAME_TO_CLASS:
                continue
            state_module = __import__('state.' + NAME_TO_CLASS[name], fromlist=[''])
            state_class = getattr(state_module, NAME_TO_CLASS[name], None)
            state = state_class(name, self.entity, config.get(name))
            self.state_map[name] = state

    def check_current_state(self, state_name):
        if self.cur_state is None:
            return False
        if state_name == self.cur_state.get_name():
            return True
        return False

    def get_current_state_name(self):
        if self.cur_state is None:
            return 'null'
        return self.cur_state.get_name()

    def can_enter_state(self, state_name):
        # 首先检查子状态
        for sub_state in self.cur_sub_states.itervalues():
            if not sub_state.can_enter_state(state_name):
                return False
        # 检查当前父状态
        cur_state = self.cur_state
        if cur_state is None:
            return True
        if cur_state.can_enter_state(state_name):
            return True
        return False
