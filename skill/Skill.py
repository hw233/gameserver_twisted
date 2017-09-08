# coding=utf-8


class Skill(object):
    def __init__(self, sid, entity):
        super(Skill, self).__init__()
        self.sid = sid  # 技能id
        self.entity = entity  # 技能属于某个实体
        # skill config
        self.config = None
        self.config = self.load_skill_config(sid)

    @staticmethod
    def load_skill_config(config_name):
        module_name = 'data.skill_data.%s' % config_name
        data_module = __import__(module_name, fromlist=[''])
        return getattr(data_module, 'data', None)

    def get_skill_config(self):
        return self.config

    def get_id(self):
        return self.sid

    def get_node_config(self, node_name):
        return self.config.get(node_name)
