# coding=utf-8
from Configuration import MaterialDB


class WeaponHandler(object):
    def __init__(self, entity):
        super(WeaponHandler, self).__init__()
        self.entity = entity
        self.weapon_map = {}
        for item_id in MaterialDB.data_map.keys():
            self.add_weapon(item_id)

    def get_attack_skill_id(self, wid):
        if wid not in self.weapon_map:
            return None
        return self.weapon_map[wid][0]

    def get_collect_skill_id(self, wid, target_id):
        if wid not in self.weapon_map:
            return None
        return self.weapon_map[wid][1].get(target_id)

    def add_weapon(self, wid):
        if wid in self.weapon_map:
            return
        config = MaterialDB.get_info_by_ID(wid)

        if self.entity.skill_handler is None:
            return
        asid = config.get('attackskill')
        if asid is not None:
            self.entity.skill_handler.add_skill(asid)

        collect_skill_map = {}
        collect_skills = config.get('collectskill')
        if collect_skills is not None:
            for d in collect_skills:
                collect_skill_map[d[1]] = d[0]
                self.entity.skill_handler.add_skill(d[0])

        self.weapon_map[wid] = [asid, collect_skill_map]
