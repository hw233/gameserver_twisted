'''
@describe :
           each of the object on the ground should have a backpack manager.
'''

class BackpackManager(object):
    def __init__(self, max_block = 16):
        super(BackpackManager, self).__init__()
        self.Weapon = None
        self.Armor = None
        self.Hat = None
        self.backpack = {}
        self.max_block = 16

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

    def take_away(self, ID, num):
        '''
        :param ID: backpack ID
        :return: do not have any return None
        '''
        if self.backpack.has_key(ID) is False or num > self.backpack[ID].num:
            return None

        obj = self.backpack[ID]
        if obj.num == num:
            del self.backpack[ID]
            return obj
        # Not Implemented ****************




