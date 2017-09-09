# coding=utf-8
#    "futou" : {
#        "ID" : 2001,
#        "name" : '斧头',
#        "describe" : '可以用来砍树和砍...人。',
#        "icon_name" : 'futou',
#        "pile_bool" : False,               #是否可叠加
#        "attack" : 10,                     #攻击力，武器，护甲有效\
#        "attackskill":1001,				#攻击技能ID
#		 ”collectskill":[[1002,3], [1002,7]],         #针对3号与7号场景物件，使用ID为1002号技能
#        "attack_speed" : 0,                #攻击速度加成，武器有效
#        "move_speed" : 0,                  #移动速度加成，护甲有效
#        "make_speed" : 0,                  #制作时间，需要制作的物品
#        "defense" : 0,                     #防御加成，护甲有效
#        "costblood" : 5,                    #每次使用消耗物品的生命，物品生命默认为100，可使用物品有效，如果是护甲，则是每次被攻击掉的生命值
#		 “food":20,                          #食用之后，加成体力。
#        "make_list": {1001:1, 1002:1},      #制作材料，可制作物品有效
#    },

material_DB = {
    '''*****************************Materials**********************Begin'''
    "shuzhi": {
        "ID": 1001,
        "name": '树枝',
        "describe": '随随便便从野外捡到的树枝，似乎可以拿来造点什么。',
        "pile_bool": True,
        "icon_name": "1001.png",
        "item": 11,
    },
    "mutou": {
        "ID": 1002,
        "name": '木头',
        "describe": '一截从树上砍下来的木头，可以用来制作各种工具。',
        "pile_bool": True,
        "icon_name": "1002.png",
        "item": 10,
    },
    "cao": {
        "ID": 1003,
        "name": '草',
        "describe": '一截从树上砍下来的木头，可以用来制作各种工具。',
        "pile_bool": True,
        "icon_name": "1003.png",
        "item": 6,
    },
    "shitou": {
        "ID": 1004,
        "name": '石头',
        "describe": '坚硬的石头，丢石头不是正道，你要蓄力丢那更坏了！',
        "pile_bool": True,
        "icon_name": "1004.png",
        "attackskill": 10040,
        "gim": "model/stone/stone_03.gim",
        "item": 105,
        'socket': 'weapon',
    },
	"tie": {
        "ID": 1005,
        "name": '铁',
        "describe": '一截从树上砍下来的木头，可以用来制作各种工具。',
        "pile_bool": True,
        "icon_name": "1003.png",
        "item": 6004,
    },
}

weapon_DB = {
    "shou": {
        "ID": 2000,
        "name": '手',
        "describe": '空手。',
        "icon_name": '2001.png',
        "gim": "",
        "pile_bool": False,  # 是否可叠加
        "attack": 0,  # 攻击力
        "attackskill": 2000,  # 攻击技能ID
        "collectskill": [[101, 7], [101, 8]],
    },
    "futou": {
        "ID": 2001,
        "name": '斧头',
        "describe": '可以用来砍树和砍...人。',
        "icon_name": '2001.png',
        "gim": "model/axe/axe_obj.gim",
        "item": 2001,
        "pile_bool": False,  # 是否可叠加
        "attack": 15,  # 攻击力
        "attackskill": 1000,  # 攻击技能ID
        "collectskill": [[2001, 7], [2001, 8]],
        "make_speed": 2,  # 制作时间
        "costblood": 25,  # 每次使用消耗物品的生命，物品生命默认为100
        "make_list": {1001: 2, 1004: 4},  # 制作材料
    },
    "chuizi": {
        "ID": 2002,
        "name": '锤子',
        "describe": '能把人打倒的大锤子',
        "icon_name": "2002.png",
        "gim": "model/hammer/hammer.gim",
        "item": 2002,
        "pile_bool": False,
        "attack": 25,  # 攻击力
        "attackskill": 1002,  # 攻击技能ID
        "make_speed": 4,  # 制作时间
        "costblood": 25,  # 每次使用消耗物品的生命，物品生命默认为100
        "make_list": {1002: 2, 1004: 4},  # 制作材料
    },
    "biaoqiang": {
        "ID": 2003,
        "name": '标枪',
        "describe": '投掷的标枪',
        "icon_name": "2003.png",
        "gim": "model/lance/lance.gim",
        "item": 2003,
        "pile_bool": True,
        "attack": 15,  # 攻击力
        "attackskill": 1003,  # 攻击技能ID
        "make_speed": 2,  # 制作时间
        "costblood": 100,  # 每次使用消耗物品的生命，物品生命默认为100
        "make_list": {1002: 2, 1003: 2},  # 制作材料
    },

    "bishou": {
        "ID": 2004,
        "name": '匕首',
        "describe": '伤害很高的近战武器',
        "icon_name": "2004.png",
        "gim": "model/branch/branch.gim",
        "item": 2004,
        "pile_bool": True,
        "attack": 20,  # 攻击力
        "make_speed": 2,  # 制作时间
        "costblood": 4,  # 每次使用消耗物品的生命，物品生命默认为100
    },
}

armor_DB = {
    "mudunpai": {
        "ID": 3001,
        "name": '木盾牌',
        "describe": '并不是很坚硬的护甲',
        "icon_name": '3001.png',
        "gim": "model/shield/shield.gim",
        "item": 3001,
        "pile_bool": False,
        "defense": 15,
        "costblood": 5,
        "make_list": {1002: 2, 1003: 2},
    },
    "tiedunpai": {
        "ID": 3002,
        "name": '铁盾牌',
        "describe": '稍微坚硬点护甲',
        "icon_name": '3001.png',
        "gim": "model/shield/shield.gim",
        "item": 3002,
        "pile_bool": False,
        "defense": 30,
        "costblood": 4,
        "make_list": {1002: 6, 1004: 4},
    },
}

hat_DB = {
    "maozi": {
        "ID": 4001,
        "name": '帽子',
        "describe": '带上奇特颜色的帽子，防御会更强!',
        "icon_name": '4001.png',
        "gim": "model/hat/hat.gim",
        "item": 4001,
        "pile_bool": False,
        "defense": 10,
        "costblood": 2,
        "make_list": {1001: 2, 1002: 2},
    },
    "haomaozi": {
        "ID": 4002,
        "name": '更强的帽子',
        "describe": '带上最强的帽子，就是最强的！',
        "icon_name": '4001.png',
        "gim": "model/hat/hat.gim",
        "item": 4002,
        "pile_bool": False,
        "costblood": 4,
        "defense": 20,
        "make_list": {1002: 2, 1003: 2},
    },
}

trap_DB = {
    "muzhixianjing": {
        "ID": 5001,
        "name": '木制陷阱',
        "describe": '布置完之后，非常的可怕！',
        "icon_name": '5001.png',
        "gim": "model/branch/branch.gim",
        "drop_gim": "model/hat/hat.gim",
        "pile_bool": True,
        "attack": 40,
        # "attackskill": 5001,
        "health": 100,
        "make_list": {1002: 4, 1004: 4},
    },

    "jingzhixianjing": {
        "ID": 5002,
        "name": '精致陷阱',
        "describe": '可怕的陷阱',
        "gim": "model/branch/branch.gim",
        "drop_gim": "model/hat/hat.gim",
        "icon_name": '5001.png',
        "pile_bool": True,
        "attack": 60,
        # "attackskill": 5001,
        "health": 100,
        "make_list": {1002: 4, 1004: 4},
    },
}

food_DB = {
    "jiangguo": {
        "ID": 6001,
        "name": '浆果',
        "describe": '味道微甜的果子',
        "icon_name": '6001.png',
        "gim": "model/berry/berry_01.gim",
        "item": 3,
        "pile_bool": True,
        "attackskill": 60010,
        "attack": 5,  # 攻击力
        "collectskill": [[60011, -1]],  # 场景对象为-1为吃东西
        'socket': 'weapon',  # 挂接点名字，没有此项默认为weapon
    },

    "niaodan": {
        "ID": 6002,
        "name": '鸟蛋',
        "describe": '大鸟留下来的蛋，可以吃。丢人据说可以加血',
        "icon_name": '6002.png',
        "gim": "model/egg/egg.gim",
        "item": 6002,
        "pile_bool": True,
        "attackskill": 60020,
        # "food": 50,
        "collectskill": [[60021, -1]],  # 场景对象为-1为吃东西
        "attack": 40,
        'socket': 'weapon',
    },

    "darou": {
        "ID": 6003,
        "name": '大肉',
        "describe": '美味的大肉，生吃也不是不可以',
        "icon_name": '6003.png',
        "gim": "model/meat/meat.gim",
        "item": 6003,
        "pile_bool": True,
        "collectskill": [[60031, -1]],  # 场景对象为-1为吃东西
        "attack": 80,
        'socket': 'weapon',
    },
}


class MaterialDB(object):
    def __init__(self):
        super(MaterialDB, self).__init__()
        self.ID_to_data_map = {}

        self.ID_to_material_data_map = {}
        self.ID_to_weapon_data_map = {}
        self.ID_to_armor_data_map = {}
        self.ID_to_trap_data_map = {}
        self.ID_to_hat_data_map = {}
        self.ID_to_food_data_map = {}

        self.load_all_info()

    def load_all_info(self):
        for v in material_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_material_data_map[v["ID"]] = v

        for v in weapon_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_weapon_data_map[v["ID"]] = v

        for v in armor_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_armor_data_map[v["ID"]] = v

        for v in trap_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_trap_data_map[v["ID"]] = v

        for v in hat_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_hat_data_map[v["ID"]] = v

        for v in food_DB.itervalues():
            self.ID_to_data_map[v["ID"]] = v
            self.ID_to_food_data_map[v["ID"]] = v

    def get_info_by_ID(self, ID):
        if self.ID_to_data_map.has_key(ID) is False:
            return None

        return self.ID_to_data_map[ID]

    def get_material_info_by_ID(self, ID):
        if self.ID_to_material_data_map.has_key(ID) is False:
            return None

        return self.ID_to_material_data_map[ID]

    def get_weapon_info_by_ID(self, ID):
        if self.ID_to_weapon_data_map.has_key(ID) is False:
            return None

        return self.ID_to_weapon_data_map[ID]

    def get_armor_info_by_ID(self, ID):
        if self.ID_to_armor_data_map.has_key(ID) is False:
            return None

        return self.ID_to_armor_data_map[ID]

    def get_trap_info_by_ID(self, ID):
        if self.ID_to_trap_data_map.has_key(ID) is False:
            return None

        return self.ID_to_trap_data_map[ID]

    def get_hat_info_by_ID(self, ID):
        if self.ID_to_hat_data_map.has_key(ID) is False:
            return None

        return self.ID_to_hat_data_map[ID]

    def get_food_info_by_ID(self, ID):
        if self.ID_to_food_data_map.has_key(ID) is False:
            return None

        return self.ID_to_food_data_map[ID]

    def get_all_makable_ID(self):
        result = []
        for id, value in self.ID_to_data_map.items():
            if value.has_key("make_list") is True:
                result.append(id)

        return result

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls._instance = super(MaterialDB, cls).__new__(cls, *args, **kwargs)

        return cls._instance


material_db = MaterialDB()

data_map = material_db.ID_to_data_map
get_info_by_ID = material_db.get_info_by_ID
get_material_info_by_ID = material_db.get_material_info_by_ID
get_weapon_info_by_ID = material_db.get_weapon_info_by_ID
get_armor_info_by_ID = material_db.get_armor_info_by_ID
get_trap_info_by_ID = material_db.get_trap_info_by_ID
get_hat_info_by_ID = material_db.get_hat_info_by_ID
get_food_info_by_ID = material_db.get_food_info_by_ID
get_all_makable_ID = material_db.get_all_makable_ID
