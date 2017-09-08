# coding=utf-8
from Creature import Creature
from common.events import MsgSCPlayerBorn
from Managers.BackpackManager import BackpackManager
from common.vector import Vector3
from component.SkillHandler import SkillHandler
from component.WeaponHandler import WeaponHandler
from common import DebugAux


# class PlayerAttributes(object):
#     def __init__(self, attack, defense, attack_speed, move_speed, make_speed, collect_speed):
#         super(PlayerAttributes, self).__init__()
#         self.attack = attack
#         self.defense = defense
#         self.attack_speed = attack_speed
#         self.move_speed = move_speed
#         self.make_speed = make_speed
#         self.collect_speed = collect_speed


class Player(Creature):
    def __init__(self, client_hid, name, position, rotation, config, group_id, arena):
        super(Player, self).__init__(config['health'], position, rotation, group_id, arena)

        self.client_hid = client_hid
        self.name = name

        # properties
        self.spirit = config['spirit']
        self.attack = config['attack']
        self.defense = config['defense']
        self.body_radius = config['body_radius']

        self.default_move_speed = config['move_speed']
        self.move_velocity = Vector3(0, 0, 0)

        self.accelerate_velocity = Vector3(0, 0, 0)

        # self.attack_speed = config['attack_speed']
        # self.make_speed = config['make_speed']
        # self.collect_speed = config['collect_speed']

        # components
        self.backpack_manager = BackpackManager()

        # skill handler
        self.skill_handler = SkillHandler(self)

        # weapon handler
        self.weapon_handler = WeaponHandler(self)

        self.is_leave_scene = False

    def update(self):
        pass

    def spirit_update(self):
        pass

    def add_weapon(self, wid):
        self.weapon_handler.add_weapon(wid)

    def debug_base_attack(self):
        return object.__getattribute__(self, "attack")

    def debug_weapon_attack(self):
        return self.backpack_manager.debug_weapon_attack()

    def debug_base_defense(self):
        return self.backpack_manager.debug_defense()

    def generate_born_msg(self, send_to_others):
        return MsgSCPlayerBorn(self.entity_id, send_to_others, self.name, self.health, self.position.x,
                               self.position.y, self.position.z, self.rotation.x, self.rotation.y, self.rotation.z)

    def set_leave_scene(self):
        self.is_leave_scene = True

    def is_dead(self):
        if self.is_leave_scene:
            return True
        return self.health <= 0

    def add_spirit(self, val, spirit):
        self.spirit = self.spirit + int(val * spirit)
        if self.spirit > 100:
            self.spirit = 100

    def set_position(self, pos):
        if self.is_dead():
            return
        super(Player, self).set_position(pos)

    def set_rotation(self, rot):
        if self.is_dead():
            return
        super(Player, self).set_rotation(rot)

    def get_backpack_syn_message(self):
        from common.events import MsgSCBackpackSyn

        msg = self.backpack_manager.generate_backpack_syn_message_ex()
        data = msg.marshal()

        cc = MsgSCBackpackSyn()
        cc.unmarshal(data)

        self.backpack_manager.parse_backpack_syn_message_ex(cc)

        return msg

    def get_attack_value(self, weapon_deduce=True):
        if hasattr(self, "attack") is False:
            return

        if weapon_deduce is True:
            DebugAux.Log("[server] [player] True")
            return self.attack + self.backpack_manager.get_attack()
        else:
            DebugAux.Log("[server] [player] False")
            return self.attack + self.backpack_manager.debug_weapon_attack()
