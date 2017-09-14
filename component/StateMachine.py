# coding=utf-8
from common import conf


class StateMachine(object):
    def __init__(self, entity, config_file_name):
        super(StateMachine, self).__init__()
        self.entity = entity
        self.cur_state = conf.STATE_IDLE  # 父状态，只能有一个
        self.cur_sub_states = []  # 子状态，可以有多个
        self.config = __import__(config_file_name, fromlist=['']).data

    def check_cur_state(self, name):
        return self.cur_state == name

    def set_all_states(self, states):
        s = states.split('|')
        self.set_cur_state(s[0])
        if len(s[1]) > 0:
            self.set_sub_states(s[1].split(','))

    def pack_all_states(self):
        s = self.cur_state + '|'
        return s + ','.join(self.cur_sub_states)

    def set_sub_states(self, state_names):
        self.cur_sub_states = []
        for name in state_names:
            self.cur_sub_states.append(name)

    def set_cur_state(self, state_name):
        self.cur_state = state_name

    def can_enter_state(self, state_name):
        # 首先检查子状态
        for sub_state in self.cur_sub_states:
            if self.config.get(sub_state).get(state_name, 0) == 1:
                return False
        # 检查当前父状态
        cur_state = self.cur_state
        if cur_state is None:
            return True
        if self.config.get(cur_state).get(state_name, 0) != 1:
            return True
        return False

    def change_state(self, state_name):
        """
        转换状态
        """
        self.cur_state = state_name

        # delete sub states
        del_names = []
        for sub_state_name in self.cur_sub_states:
            if self.config.get(self.cur_state).get(sub_state_name, 0) == 2:
                del_names.append(sub_state_name)
        for name in del_names:
            self.cur_sub_states.remove(name)
