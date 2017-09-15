# coding=utf-8

monster_db = [
    {
        # 掉铁的头目
        'ID': 100,
        'move_speed': 200,  # cm/s
        'health': 500,
        'attack': 25,
        'body_radius': 50,  # cm
        'lock_distance': 600,
		'unlock_distance': 1800,
		'walk_distance': [600, 1200],
        'model_name': "model/monster/monster01.gim",
        'monster_name': "drop_iron",
        'drop_items': {1005: 3, 6003: 1},
        'skill': {20001: 0.7, 20002: 0.3}
    },
    {
        # 追击的怪物01
        'ID': 101,
        'move_speed': 300,  # cm/s
        'health': 50,
        'attack': 6,
        'body_radius': 50,  # cm
        'lock_distance': 800,
		'walk_distance': [300, 1000],
		'unlock_distance': 3000,
        'model_name': "model/monster/monster02.gim",
        'monster_name': "runner01",
        'skill': {20003: 1},
		'drop_items': {1005: 0},
        # 'drop_items':{1005:1, 1002:1},
    },
    {
        # 追击的怪物02
        'ID': 102,
        'move_speed': 300,  # cm/s
        'health': 150,
        'attack': 12,
        'body_radius': 50,  # cm
        'lock_distance': 800,
		'walk_distance': [300, 1000],
		'unlock_distance': 3000,
        'model_name': "model/monster/monster03.gim",
        'monster_name': "runner02",
        'skill': {20003: 1},
		'drop_items': {1005: 0},
        # 'drop_items':{1005:1, 1002:1},
    },
	{
		# 追击的怪物03
        'ID':103,
        'move_speed': 300,  # cm/s
        'health': 500,
        'attack': 21,
        'body_radius': 50,  # cm
        'lock_distance':800,
		'unlock_distance': 3000,
		'walk_distance': [300, 1000],
        'model_name': "model/monster/monster04.gim",
        'monster_name': "runner02",
		'skill':{20003:1},
		'drop_items': {1005: 0},
        #'drop_items':{1005:1, 1002:1},
    },
	{
		# 兔子
        'ID':201,
        'move_speed': 100,  # cm/s
        'health': 1,
        'attack': 1,
        'body_radius': 5,  # cm
        'lock_distance': 0,
        'unlock_distance': 100,
		'walk_distance': [300, 600],
        'model_name': "model/rabbit/rabbit.gim",
        'monster_name': "rabbit",
        'drop_items': {6003: 1},
    },
]


class MonsterDB(object):
    def __init__(self):
        super(MonsterDB, self).__init__()

        self.ID_to_info_map = {}

        self.init()

    def init(self):
        for cell in monster_db:
            self.ID_to_info_map[cell["ID"]] = cell

    def get_info_by_ID(self, ID):
        if ID in self.ID_to_info_map:
            return self.ID_to_info_map[ID]

        return None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MonsterDB, cls).__new__(cls, *args, **kwargs)

        return cls._instance


__monster_db = MonsterDB()

get_info_by_ID = __monster_db.get_info_by_ID
