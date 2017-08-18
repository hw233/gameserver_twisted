material_DB = {
    '''*****************************Materials**********************Begin'''
    "mutou":{
        "ID" : 1001,
        "name" : '木头',
        "describe" : '测试',
        "icon_num" : 1001,
        "trade_bool" : True,
        "pile_bool" : True,
    },

    "shuzhi" : {
        "ID" : 1002,
        "name" : '树枝',
        "describe" : '测试',
        "icon_num" : 1002,
        "trade_bool" : True,
        "pile_bool" : True,
    },
    '''*****************************Materials**********************End'''
    
    '''*****************************Weapon**********************Begin'''
    "futou" : {
        "ID" : 2001,
        "name" : '斧头',
        "describe" : '测试',
        "icon_num" : 2001,
        "trade_bool" : True,
        "buy_price" : 0,
        "sell_price" : 0,
        "pile_bool" : False,
        "attack" : 10,
        "attack_speed" : 0,
        "move_speed" : 0,
        "make_speed" : 0,
        "collect_speed" : 0,
        "defense" : 0,
        "health" : 100,
        "make_list": [1001, 1002],
    },
    '''*****************************Weapon**********************End'''
    
    '''*****************************Armor**********************Begin'''
    "caojia" : {
        "ID" : 3001,
        "name" : '草甲',
        "describe": '测试',
        "icon_num" : 3001,
        "trade_bool" : True,
        "buy_price" : 0,
        "sell_price" : 0,
        "pile_bool" : False,
        "attack" : 0,
        "attack_speed" : 0,
        "move_speed" : 0,
        "make_speed" : 0,
        "collect_speed" : 0,
        "defense" : 0,
        "health" : 100,
        "make_list" : [1001, 1002],
    },
    '''*****************************Armor**********************End'''
    
    '''*****************************Trap**********************Begin'''
    "muzhixianjing" : {
        "ID" : 4001,
        "name" : '木制陷阱',
        "describe": '测试',
        "icon_num" : 4001,
        "trade_bool" : True,
        "buy_price" : 0,
        "sell_price" : 0,
        "pile_bool" : False,
        "attack" : 0,
        "attack_speed" : 0,
        "move_speed" : 0,
        "make_speed" : 0,
        "collect_speed" : 0,
        "defense" : 0,
        "health" : 100,
        "make_list" : [1001, 1002],
    },

    "jingzhixianjing" : {
        "ID" : 4001,
        "name" : '精致陷阱',
        "describe": '测试',
        "icon_num" : 4001,
        "trade_bool" : True,
        "buy_price" : 0,
        "sell_price" : 0,
        "pile_bool" : False,
        "attack" : 0,
        "attack_speed" : 0,
        "move_speed" : 0,
        "make_speed" : 0,
        "collect_speed" : 0,
        "defense" : 0,
        "health" : 100,
        "make_list" : [1001, 1002],
        },
}


class MaterialDB(object):
    def __init__(self):
        super(MaterialDB, self).__init__()
        self.ID_to_data_map={}
        self.load_all_info()

    def load_all_info(self):
        for v in material_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v

    def get_info_by_ID(self, ID):
        if self.ID_to_data_map.has_key(ID) is False:
            return None

        return self.ID_to_data_map[ID]

material_db = MaterialDB()



