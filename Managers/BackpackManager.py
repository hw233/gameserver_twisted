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


class BackpackManager(object):
    def __init__(self, max_block = 16):
        super(BackpackManager, self).__init__()

        self.weapon = None
        self.armor = None
        self.hat = None

        self.backpack = {}
        self.max_block = max_block

    def import_obj_from(self, bp_manager, ID, num):
        '''
        :param bp_manager: another entity's backpack
        :param ID: trade item ID
        :param num: trade item num
        :return: success return true else false
        '''

        obj = bp_manager.take_away(ID, num)
        if obj is None:
            return False

        if self.bring_in(obj) is False:
            bp_manager.bring_in(obj)
            return False

        return True

    def export_obj_to(self, bp_manager, ID, num):
        '''
        :param bp_manager: another entity's backpack
        :param ID: trade item ID
        :param num: trade item num
        :return: success return true else false
        '''

        obj = self.take_away(ID, num)

        if obj is None:
            return False

        if bp_manager.bring_in(obj) is False:
            self.bring_in(obj)
            return False

        return True

    def bring_in(self, obj):
        '''
        :param obj: new obj will add into the backpack
        :return: operation success return True else return False
        '''
        if len(self.backpack) >= self.max_block:
            return False

        if obj.pile_bool is False or self.backpack.has_key(obj.ID) is False:
            self.backpack[obj.ID] = obj

        self.backpack[obj.ID].pile(obj)

        return True

    def take_away(self, ID, num):
        '''
        :param ID: backpack ID
        :return: if success return obj with num objects else return None
        '''
        if self.backpack.has_key(ID) is False or num > self.backpack[ID].num:
            return None

        obj = self.backpack[ID]
        if obj.num == num:
            del self.backpack[ID]
            return obj

        return obj.split(num)

    def install_weapon(self, ID):
        '''
        :param ID: weapon ID
        :return: None
        '''
        weapon = self.take_away(ID)

        if weapon is not None:
            self.weapon = weapon

    def uninstall_weapon(self):
        '''
        :return: if success return true else return false
        '''

        if len(self.backpack) < self.max_block and self.weapon is not None:
            self.bring_in(self.weapon)
            self.weapon = None
            return True

        return False

    def install_armor(self, ID):
        '''
        :param ID: armor ID
        :return: None
        '''
        armor = self.take_away(ID)

        if armor is not None:
            self.armor = armor

    def uninstall_armor(self):
        '''
        :return: if success return true else return false
        '''

        if len(self.backpack) < self.max_block and self.armor is not None:
            self.bring_in(self.armor)
            self.armor = None
            return True

        return False

    def install_hat(self, ID):
        '''
        :param ID: armor ID
        :return: None
        '''
        hat = self.take_away(ID)

        if hat is not None:
            self.hat = hat

    def uninstall_hat(self):
        '''
        :return: if success return true else return false
        '''

        if len(self.backpack) < self.max_block and self.hat is not None:
            self.bring_in(self.hat)
            self.hat = None
            return True

        return False
