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


class BackpackManager(object):
    def __init__(self, max_block = 100):
        super(BackpackManager, self).__init__()

        self.weapon = None
        self.armor = None
        self.hat = None

        self.active_index = -1 # (-1,0,1,2) if -1 no active object

        self.entity_id_to_backpack_obj_map = {}
        self.max_block = max_block

        self.init()
        self._just_for_test_delete_me()

    def init(self):
        self.weapon = []
        self.weapon.append(None)
        self.weapon.append(None)
        self.weapon.append(None)

    def _just_for_test_delete_me(self):
        item = BPItemObject(1001, 10)
        self.bring_in_ex(item)

        item = BPItemObject(1002, 10)
        self.bring_in_ex(item)

        item = BPItemObject(2002, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2002, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2003, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2004, 2)
        self.bring_in_ex(item)

        item = BPItemObject(2004, 2)
        self.bring_in_ex(item)

        item = BPItemObject(3001, 2)
        self.bring_in_ex(item)

        item = BPItemObject(4001, 2)
        self.bring_in_ex(item)

        hat = BPItemObject(4001, 1)
        self.hat = hat

        armor = BPItemObject(3001, 1)
        self.armor = armor

    def get_item_num_by_ID(self, ID):
        num = 0
        for value in self.entity_id_to_backpack_obj_map.itervalues():
            if value.ID == ID:
                num += value.num
        return num

    def get_entity_id_by_ID(self, ID):
        for key,value in self.entity_id_to_backpack_obj_map.items():
            if value.ID == ID:
                return key

        return None

    def bring_in_ex(self, obj):
        if obj.pile_bool is False:
            self.entity_id_to_backpack_obj_map[obj.entity_id] = obj
            return
        else:
            for v in self.entity_id_to_backpack_obj_map.itervalues():
                if v.ID == obj.ID:
                    v.num += obj.num
                    return
            self.entity_id_to_backpack_obj_map[obj.entity_id] = obj

    def take_away_ex(self, entity_id, num = 1):
        if entity_id in self.entity_id_to_backpack_obj_map:
            item = self.entity_id_to_backpack_obj_map[entity_id]
            if item.pile_bool is False:
                del self.entity_id_to_backpack_obj_map[entity_id]
            else:
                if item.num <= num:
                    del self.entity_id_to_backpack_obj_map[entity_id]
                else:
                    self.entity_id_to_backpack_obj_map[entity_id].num -= num

            return item

        return None

    def get_active_weapon(self):
        if self.active_index<0 and self.active_index>2:
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
            return False

        if slots_index < 0 or slots_index > 2:
            return False

        for k in xrange(0, 3):
            if self.weapon[k] and self.weapon[k].ID == item.ID:
                 if k == slots_index:
                    self.bring_in(self.weapon[k])
                    item = self.take_away_ex(item.entity_id, item.num)
                    self.weapon[k] = item
                    self.active_index = slots_index
                    return True

        if self.weapon[slots_index] is not None:
            self.bring_in_ex(self.weapon[slots_index])

        item = self.take_away_ex(item.entity_id, item.num)
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
                self.bring_in_ex(item)
                return item

        if self.armor is not None and self.armor.entity_id == entity_id:
            item = self.armor
            self.armor = None
            self.bring_in_ex(item)
            return item

        if self.hat is not None and self.hat.entity_id == entity_id:
            item = self.hat
            self.hat = None
            self.bring_in_ex(item)
            return item

        return None

    def install_armor_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return None

        item = self.entity_id_to_backpack_obj_map[entity_id]

        if self.armor:
            self.bring_in_ex(self.armor)
            self.armor = None

        self.armor = self.take_away_ex(item.entity_id, item.num)

        return self.armor

    def install_hat_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return None

        item = self.entity_id_to_backpack_obj_map[entity_id]

        if self.hat:
            self.bring_in_ex(self.hat)
            self.hat = None

        self.hat = self.take_away_ex(item.entity_id, item.num)

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
        print data

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

        if left_num > left_num_total or right_num > right_num_total:
            return None

        left_entity_id = self.get_entity_id_by_ID(left_id)
        right_entity_id = self.get_entity_id_by_ID(right_id)

        self.take_away_ex(left_entity_id, left_num)
        self.take_away_ex(right_entity_id, right_num)

        item = BPItemObject(ID, num)
        self.bring_in_ex(item)

        return item

    def drop_object_ex(self, entity_id):
        if entity_id not in self.entity_id_to_backpack_obj_map:
            return False

        item = self.entity_id_to_backpack_obj_map[entity_id]

        item = self.take_away_ex(item.entity_id, item.num)

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

        return val

    def get_attack(self):
        val = 0

        active_weapon = self.get_active_weapon()

        if active_weapon is not None:
            val += active_weapon.get_attack()

        if self.hat is not None:
            val += self.hat.get_attack()

        if self.armor is not None:
            val += self.armor.get_attack()

        return val

    def inquire_weapon_die(self):
        die_id_list = []
        active_weapon = self.get_active_weapon()

        if active_weapon is not None and active_weapon.health<=0:
            die_id_list.append(self.weapon[self.active_index].ID)
            self.weapon[self.active_index] = None
            self.active_index = -1

        if self.hat is not None and self.hat.health<=0:
            die_id_list.append(self.hat.ID)
            self.hat = None

        if self.armor is not None and self.armor.health<=0:
            die_id_list.append(self.armor.ID)
            self.armor = None

        return die_id_list

    def active_weapon(self, entity_id):
        for index in xrange(0, 3):
            if self.weapon[index] is not None and self.weapon[index].entity_id == entity_id:
                self.active_index = index
                return self.weapon[index]
        return None