# coding=utf-8
import math

from common import conf
from common.vector import Vector3
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

    def get_skill_node_config(self, sid, node_name):
        return self.skills[sid].get_node_config(node_name)

    def parse_move_node(self, sid, move_node_name):
        node_config = self.get_skill_node_config(sid, move_node_name)

        speed_args = node_config.get('args')
        speed = speed_args[0]
        speed_duration = speed_args[1]
        face_to = node_config.get('faceto')

        if face_to is not None:  # 寻找目标并面向它
            self.entity.attack_face_to(face_to)
        # 设定技能速度

        # 这里暂时不管持续速度！！！！！！ FIX ME !!!
        angle = self.entity.get_rotation().y
        direct = Vector3(math.sin(angle), 0, math.cos(angle))
        self.entity.set_move_velocity(direct * speed)

    def handle_attack_hit(self, sid, node_name, tag, hit_idx, hit_time):
        node_config = self.get_skill_node_config(sid, node_name)
        damage_data = node_config.get('damage')

        if damage_data is None:
            return []

        if damage_data.get('sector') is not None:  # 范围攻击
            return self.invoke_aoe(sid, node_name, damage_data, node_config, tag, hit_idx, hit_time)

        return []

    def invoke_aoe(self, sid, node_name, damage_data, node_config, tag, hit_idx, hit_time):
        if self.entity.is_dead():
            return []
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
            # print 'no targets --------- '
            return []

        if conf.DR_OPEN:
            self.entity.arena.handle_player_hit_move(self.entity.get_position(), damage_targets, node_config, hit_time)

        self.entity.arena.handle_aoe_hit(self.entity, damage_targets, damage_data, sid, node_name, tag, hit_idx)

        return damage_targets
