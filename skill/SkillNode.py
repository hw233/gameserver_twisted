# coding=utf-8
import weakref


class SkillNode(object):
    def __init__(self, skill, node_name, node_config):
        super(SkillNode, self).__init__()
        self.skill = weakref.ref(skill)
        self.entity = skill.entity
        self.node_name = node_name
        self.node_config = node_config

    def start(self, params=None):
        pass

    def run_next_nodes(self, node_names, params=None):
        self.skill().run_nodes(node_names, params)
