'''
@describe :
           each of the object on the ground should have a backpack manager.
@author :
         sai
@log:
     1. 2017-08-12 create
     2. 2017-08-14 basic func finished include 'weapon' 'armor' 'hat'
     3. 2017-08-15 implement 'import_obj_from' and 'export_obj_to'
'''
from GameObject.BPItemObject import BPItemObject
from Configuration import MaterialDB
from GameObject.GameObject import GameObject
from common import DebugAux, conf


class BackpackManager(GameObject):

    BP_INSTALL_UNINSTALL_LISTENER = 0
    BP_QUANTITY_CHANGE_LISTENER = 1
    BP_TAKE_AWAY_LISTENER = 2
    BP_BRING_IN_LISTENER = 3

    def __init__(self,parent=None, max_block = 100):
        super(BackpackManager, self).__init__()

        self.parent = parent

        self.weapon = None
        self.armor = None
        self.hat = None

        self.active_index = -1 # (-1,0,1,2) if -1 no active object

        self.entity_id_to_backpack_obj_map = {}
        self.max_block = max_block

        self.init()

        if conf.DEBUG_BILLIONAIRE:
            self._just_for_test_delete_me()

    def debug_weapon_attack(self):
        weapon = self.get_active_weapon()
        if weapon is None:
            return 0

        if hasattr(weapon, "attack"):
            return weapon.attack

    def debug_defense(self):
        num = 0
        if self.armor is not None:
            if hasattr(self.armor, "defense"):
                num += self.armor.defense

        if self.hat is not None:
            if hasattr(self.hat, "defense"):
                num += self.hat.defense

        return num

    def init(self):
        self.weapon = []
        self.weapon.append(None)
        self.weapon.append(None)
        self.weapon.append(None)

    def gm_add_item(self, ID, num):

        info = MaterialDB.get_info_by_ID(ID)
        if info is None:
            return False

        if info["pile_bool"] is False:
            for k in xrange(0, num):
                item = BPItemObject(ID)
                self.bring_in_ex(item, 1, True)
        else:
            item = BPItemObject(ID, num)
            self.bring_in_ex(item, num, True)

        return True

    def _just_for_test_delete_me(self):
        item = BPItemObject(1001, 10)
        self.bring_in_ex(item)

        item = BPItemObject(1002, 10)
        self.bring_in_ex(item)

        item = BPItemObject(6002, 10)
        self.bring_in_ex(item)

        item = BPItemObject(2001, 1)
        self.bring_in_ex(item)

        item = BPItemObject(2002, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2002, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2003, 100)
        self.bring_in_ex(item)

        item = BPItemObject(3001, 2)
        self.bring_in_ex(item)

        item = BPItemObject(4001, 2)
        self.bring_in_ex(item)

        item = BPItemObject(6001, 10)
        self.bring_in_ex(item)

        item = BPItemObject(6003, 10)
        self.bring_in_ex(item)

        hat = BPItemObject(4001, 1)
        self.hat = hat

        armor = BPItemObject(3001, 1)
        self.armor = armor

    def get_item_num_by_ID(self, ID):
        num = 0
        for value in self.entity_id_to_backpack_obj_map.itervalues():
            if value.ID == ID:
                info = MaterialDB.get_info_by_ID(ID)
                if info["pile_bool"] is False:
                    num += 1
                else:
                    num += value.num
        return num

    def get_entity_id_by_ID(self, ID):
        for key,value in self.entity_id_to_backpack_obj_map.items():
            if value.ID == ID:
                return key

        return None

    def bring_in_ex(self, obj, num = 1, trigger = False):
        if type(obj) is int:
            obj = BPItemObject(obj, num)

        if obj.pile_bool is False:
            self.entity_id_to_backpack_obj_map[obj.entity_id] = obj
            if trigger is True:
                self.trigger_event(BackpackManager.BP_BRING_IN_LISTENER, self.parent,
                                   obj.entity_id, obj.ID, obj.health, obj.num)
            return
        else:
            for v in self.entity_id_to_backpack_obj_map.itervalues():
                if v.ID == obj.ID:
                    v.num += obj.num

                    if trigger is True:
                        self.trigger_event(BackpackManager.BP_BRING_IN_LISTENER, self.parent,
                                           obj.entity_id, obj.ID,obj.health, obj.num)
                    return
            self.entity_id_to_backpack_obj_map[obj.entity_id] = obj

            if trigger is True:
                self.trigger_event(BackpackManager.BP_BRING_IN_LISTENER, self.parent, obj.entity_id,
                                   obj.ID, obj.health,obj.num)

    def take_away_ex(self, entity_id, num = 1, trigger = False):
        if entity_id in self.entity_id_to_backpack_obj_map:
            item = self.entity_id_to_backpack_obj_map[entity_id]
            if item.pile_bool is False:
                del self.entity_id_to_backpack_obj_map[entity_id]
            else:
                if item.num <= num:
                    del self.entity_id_to_backpack_obj_map[entity_id]
                else:
                    self.entity_id_to_backpack_obj_map[entity_id].num -= num
                    item = BPItemObject(self.entity_id_to_backpack_obj_map[entity_id].ID, num)

            if trigger is True:
                self.trigger_event(BackpackManager.BP_TAKE_AWAY_LISTENER, self.parent, item.entity_id,
                                   item.ID, item.health, item.num)
            return item

        return None

    def get_active_weapon(self):
        if self.active_index<0 or self.active_index>2:
            return None

        return self.weapon[self.active_index]

    def install_weapon_ex(self, entity_id, slots_index):
        '''
        :param entity_id: weapon entity_id
        :param slots_index: install to which slot
        :param action_type: if 0 indicate install weapon else exchange weapon location and active the moved one
        :return: success return True else return False
        '''

        if entity_id not in self.entity_id_to_backpack_obj_map:
            return False

        item = self.entity_id_to_backpack_obj_map[entity_id]

        info = MaterialDB.get_weapon_info_by_ID(item.ID)

        if info is None:
            info = MaterialDB.get_food_info_by_ID(item.ID)

        if info is None:
            info = MaterialDB.get_trap_info_by_ID(item.ID)

        if info is None:
            return False

        if slots_index < 0 or slots_index > 2:
            return False

        for k in xrange(0, 3):
            if self.weapon[k] and self.weapon[k].ID == item.ID:
                 if k == slots_index:
                    self.bring_in_ex(self.weapon[k], self.weapon[k].num, True)
                    item = self.take_away_ex(item.entity_id, item.num, True)
                    self.weapon[k] = item
                    self.active_index = slots_index
                    return True

        if self.weapon[slots_index] is not None:
            self.bring_in_ex(self.weapon[slots_index], self.weapon[slots_index].num, True)

        item = self.take_away_ex(item.entity_id, item.num, True)
        self.weapon[slots_index] = item
        self.active_index = slots_index
        return True

    def uninstall_weapon_ex(self, entity_id):
        for k in xrange(0, 3):
            if self.weapon[k] is None:
                continue

            if self.weapon[k].entity_id == entity_id:
                item = self.weapon[k]
                self.weapon[k] = None
                self.bring_in_ex(item, item.num, True)
                if self.active_index == k:
                    self.active_index = -1
                return item

        if self.armor is not None and self.armor.entity_id == entity_id:
            item = self.armor
            self.armor = None
            self.bring_in_ex(item, item.num, True)
            return item

        if self.hat is not None and self.hat.entity_id == entity_id:
            item = self.hat
            self.hat = None
            self.bring_in_ex(item, item.num, True)
            return item

        return None

    def install_armor_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return None

        item = self.entity_id_to_backpack_obj_map[entity_id]

        if self.armor:
            self.bring_in_ex(self.armor, self.armor, True)
            self.armor = None

        self.armor = self.take_away_ex(item.entity_id, item.num, True)

        return self.armor

    def install_hat_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return None

        item = self.entity_id_to_backpack_obj_map[entity_id]

        if self.hat:
            self.bring_in_ex(self.hat, self.armor, True)
            self.hat = None

        self.hat = self.take_away_ex(item.entity_id, item.num, True)

        return self.hat

    def generate_backpack_syn_message_ex(self):
        import struct
        from common.events import MsgSCBackpackSyn
        '''
        :describe:
                  1. max_block
                  2. weapon_id (-1 means illegal)
                  3. armor_id
                  4. hat_id
                  5. first_obj_id
                  6. first_obj_num
                  7. second_obj_id
                  8. second_obj_num
                  9. ..._obj_id
                  10. ..._obj_num
        :return: MsgSCBackpackSyn
        '''

        fmt = "<ii" + "iiii" * (len(self.entity_id_to_backpack_obj_map)+5)

        data = struct.pack("<i", self.max_block)
        data += struct.pack("<i", self.active_index)

        data += struct.pack("<i", self.weapon[0].ID) if self.weapon[0] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[0].entity_id) if self.weapon[0] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[0].health) if self.weapon[0] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[0].num) if self.weapon[0] else struct.pack("<i", -1)

        data += struct.pack("<i", self.weapon[1].ID) if self.weapon[1] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[1].entity_id) if self.weapon[1] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[1].health) if self.weapon[1] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[1].num) if self.weapon[1] else struct.pack("<i", -1)

        data += struct.pack("<i", self.weapon[2].ID) if self.weapon[2] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[2].entity_id) if self.weapon[2] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[2].health) if self.weapon[2] else struct.pack("<i", -1)
        data += struct.pack("<i", self.weapon[2].num) if self.weapon[2] else struct.pack("<i", -1)

        data += struct.pack("<i", self.armor.ID) if self.armor else struct.pack("<i", -1)
        data += struct.pack("<i", self.armor.entity_id) if self.armor else struct.pack("<i", -1)
        data += struct.pack("<i", self.armor.health) if self.armor else struct.pack("<i", -1)
        data += struct.pack("<i", self.armor.num) if self.armor else struct.pack("<i", -1)

        data += struct.pack("<i", self.hat.ID) if self.hat else struct.pack("<i", -1)
        data += struct.pack("<i", self.hat.entity_id) if self.hat else struct.pack("<i", -1)
        data += struct.pack("<i", self.hat.health) if self.hat else struct.pack("<i", -1)
        data += struct.pack("<i", self.hat.num) if self.hat else struct.pack("<i", -1)

        for obj in self.entity_id_to_backpack_obj_map.itervalues():
            data += struct.pack("<iiii", obj.ID, obj.entity_id, obj.health, obj.num)

        msg = MsgSCBackpackSyn(fmt, data)

        return msg

    def parse_backpack_syn_message_ex(self, msg):
        import struct
        data = struct.unpack(msg.format, msg.data)
        DebugAux.Log(data)

        self.entity_id_to_backpack_obj_map = {}

        self.max_block = data[0]
        self.active_index = data[1]

        self.weapon[0] = BPItemObject(data[2], 1) if data[2] != -1 else None
        if self.weapon[0] is not None:
            self.weapon[0].entity_id = data[3]
            self.weapon[0].health = data[4]
            self.weapon[0].num = data[5]

        self.weapon[1] = BPItemObject(data[6], 1) if data[6] != -1 else None
        if self.weapon[1] is not None:
            self.weapon[1].entity_id = data[7]
            self.weapon[1].health = data[8]
            self.weapon[1].num = data[9]

        self.weapon[2] = BPItemObject(data[10], 1) if data[10] != -1 else None
        if self.weapon[2] is not None:
            self.weapon[2].entity_id = data[11]
            self.weapon[2].health = data[12]
            self.weapon[2].num = data[13]

        self.armor = BPItemObject(data[14], 1) if data[14] != -1 else None
        if self.armor is not None:
            self.armor.entity_id = data[15]
            self.armor.health = data[16]
            self.armor.num = data[17]
            DebugAux.Log("print armor num", self.armor.num)

        self.hat = BPItemObject(data[18], 1) if data[18] != -1 else None
        if self.hat is not None:
            self.hat.entity_id = data[19]
            self.hat.health = data[20]
            self.hat.num = data[21]

        for x in xrange(22, len(data), 4):
            item = BPItemObject(data[x],1)
            item.entity_id = data[x+1]
            item.health = data[x + 2]
            item.num = data[x + 3]
            self.bring_in_ex(item)

    def make_request(self, ID, num):
        '''
        :param ID: target object id
        :param num: request make number
        :return: success return True else return False
        '''
        DebugAux.Log("[server] make request ",ID, " num ", num)
        info = MaterialDB.get_info_by_ID(ID)
        res = False

        if info["pile_bool"] is False:
            for k in xrange(0, num):
                item = self.make_object(ID)
                if item is not None:
                    res = True
        else:
            item = self.make_object(ID, num)
            if item is not None:
                res = True

        return res

    def make_object(self, ID, num=1):

        DebugAux.Log("[server] [backpack] begin")

        data = MaterialDB.get_info_by_ID(ID)
        if data is None:
            return None

        make_list = data["make_list"]

        keys = []
        values = []

        for k, v in make_list.items():
            keys.append(k)
            values.append(v)

        left_id = keys[0]
        right_id = keys[1]

        left_num = values[0] * num
        right_num = values[1] * num

        left_num_total = self.get_item_num_by_ID(left_id)
        right_num_total = self.get_item_num_by_ID(right_id)

        DebugAux.Log("[server] [backpack] ", left_num, right_num, left_num_total, right_num_total)
        if left_num > left_num_total or right_num > right_num_total:
            return None

        left_entity_id = self.get_entity_id_by_ID(left_id)
        right_entity_id = self.get_entity_id_by_ID(right_id)

        self.take_away_ex(left_entity_id, left_num, True)
        self.take_away_ex(right_entity_id, right_num, True)

        item = BPItemObject(ID, num)
        self.bring_in_ex(item, item.num, True)

        return item

    def drop_object_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return False

        item = self.entity_id_to_backpack_obj_map[entity_id]

        item = self.take_away_ex(item.entity_id, item.num, True)

        return item

    def get_defense(self):
        val = 0

        active_weapon = self.get_active_weapon()

        if active_weapon is not None:
            val += active_weapon.get_defense()

        if self.hat is not None:
            val += self.hat.get_defense()

        if self.armor is not None:
            val += self.armor.get_defense()

        self._trigger_syn_msg()

        return val

    def _trigger_syn_msg(self):
        die_list = self.inquire_weapon_die()

        if len(die_list) >= 0:
            # trigger weapon install or uninstall message
            self.trigger_event(BackpackManager.BP_INSTALL_UNINSTALL_LISTENER, self.parent, die_list)

        # trigger weapon blood msg
        self.trigger_event(BackpackManager.BP_QUANTITY_CHANGE_LISTENER, self.parent)

    def get_attack(self):
        val = 0

        active_weapon = self.get_active_weapon()

        if active_weapon is not None:
            val += active_weapon.get_attack()

        if self.hat is not None:
            val += self.hat.get_attack()

        if self.armor is not None:
            val += self.armor.get_attack()

        self._trigger_syn_msg()

        return val

    def auto_equipment(self, ID):

        weapon = None
        entity_id = None

        for entity_id, obj in self.entity_id_to_backpack_obj_map.items():
            if obj.ID == ID:
                weapon = obj
                entity_id = entity_id
                del self.entity_id_to_backpack_obj_map[entity_id]
                break

        if entity_id is not None and weapon is not None:
            if self.armor is not None and self.armor.ID == weapon.ID:
                self.armor = weapon
            elif self.hat is not None and self.hat.ID == weapon.ID:
                self.hat = weapon
            elif self.get_active_weapon() is not None:
                self.weapon[self.active_index] = weapon
            return True
        else:
            return False

    def inquire_weapon_die(self):
        die_id_list = []
        active_weapon = self.get_active_weapon()

        if active_weapon is not None and (active_weapon.health <= 0 or active_weapon.num <=0):
            if active_weapon.pile_bool is False and self.auto_equipment(active_weapon.ID) is False:
                die_id_list.append(self.weapon[self.active_index].ID)
                self.weapon[self.active_index] = None
                self.active_index = -1
            else:
                if active_weapon.num <= 0 and self.auto_equipment(active_weapon.ID) is False:
                    die_id_list.append(self.weapon[self.active_index].ID)
                    self.weapon[self.active_index] = None
                    self.active_index = -1

        if self.hat is not None and self.hat.health <= 0 and self.auto_equipment(self.hat.ID) is False:
            die_id_list.append(self.hat.ID)
            self.hat = None

        if self.armor is not None and self.armor.health <= 0 and self.auto_equipment(self.armor.ID) is False:
            die_id_list.append(self.armor.ID)
            self.armor = None

        return die_id_list

    def active_weapon(self, entity_id, action):
        if action == 0:
            if 0 <= self.active_index <= 2:
                item = self.weapon[self.active_index]
                self.active_index = -1
                return item
        else:
            for k in xrange(0,3):
                if self.weapon[k] is not None and self.weapon[k].entity_id == entity_id:
                    self.active_index = k
                    return self.weapon[k]
        return None

    def take_away_all_item(self):

        weapon = self.get_active_weapon()
        if weapon is not None:
            self.weapon[self.active_index] = None
            self.bring_in_ex(weapon)

        if self.armor is not None:
            armor = self.armor
            self.armor = None
            self.bring_in_ex(armor)

        if self.hat is not None:
            hat = self.hat
            self.hat = None
            self.bring_in_ex(hat)

        val = self.entity_id_to_backpack_obj_map
        self.entity_id_to_backpack_obj_map = {}

        return val


