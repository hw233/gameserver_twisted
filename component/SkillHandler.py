# coding=utf-8
from skill.Skill import Skill


class SkillHandler(object):
    def __init__(self, entity):
        super(SkillHandler, self).__init__()
        self.entity = entity
        self.skills = {}

    def add_skill(self, sid):
        if sid in self.skills:
            return
        skill = Skill(sid, self.entity)
        self.skills[sid] = skill

    def add_skills(self, sids):
        for sid in sids:
            self.add_skill(sid)

    def get_skill(self, sid):
        return self.skills.get(sid)

    def use_skill(self, sid):
        self.skills[sid].use()

    def get_skill_node_config(self, skill_id, node_name):
        return self.skills[skill_id].get_node_config(node_name)

    def handle_attack_hit(self, sid, node_name):
        node_config = self.get_skill_node_config(sid, node_name)
        damage_data = node_config.get('damage')

        if damage_data is None:
            return

        if damage_data.get('sector') is not None:  # 范围攻击
            self.invoke_aoe(sid, node_name, damage_data)

    def invoke_aoe(self, sid, node_name, damage_data):
        if self.entity.is_dead():
            return
        damage_targets = []

        for gid, group in self.entity.arena.group_map.iteritems():
            if gid == self.entity.get_group_id():
                continue
            for other in group:
                if other.is_dead():
                    continue
                if self.entity.in_damage_range(other, damage_data['sector']):
                    damage_targets.append(other)

        if len(damage_targets) == 0:  # 没有目标，不会触发任何伤害
            return
        self.entity.arena.handle_player_aoe_hit(self.entity, damage_targets, damage_data, sid, node_name)

