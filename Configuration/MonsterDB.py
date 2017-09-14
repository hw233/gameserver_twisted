# coding=utf-8

monster_db = [
    {
		# 掉铁的头目
        'ID':100,
        'move_speed': 400,  # cm/s
        'health': 400,
        'attack': 10,
        'body_radius': 50,  # cm
        'lock_distance':600,
        'model_name': "model/monster/monster01.gim",
        'monster_name': "drop_iron",
        'drop_items':{1005:3, 6003:1},
    },
    {
		# 追击的怪物01
        'ID':101,
        'move_speed': 400,  # cm/s
        'health': 100,
        'attack': 20,
        'body_radius': 50,  # cm
        'lock_distance':800,
        'model_name': "model/monster/monster02.gim",
        'monster_name': "runner01",
        #'drop_items':{1005:1, 1002:1},
    },
	{
		# 追击的怪物02
        'ID':102,
        'move_speed': 400,  # cm/s
        'health': 300,
        'attack': 40,
        'body_radius': 50,  # cm
        'lock_distance':800,
        'model_name': "model/monster/monster02.gim",
        'monster_name': "runner02",
        #'drop_items':{1005:1, 1002:1},
    },
	{
		# 兔子
        'ID':103,
        'move_speed': 200,  # cm/s
        'health': 1,
        'attack': 1,
        'body_radius': 5,  # cm
        'lock_distance':0,
        'model_name': "model/rabbit/rabbit.gim",
        'monster_name': "rabbit",
        'drop_items':{6003:1},
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

    def get_info_by_ID(self,ID):
        if ID in self.ID_to_info_map:
            return self.ID_to_info_map[ID]

        return None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MonsterDB, cls).__new__(cls, *args, **kwargs)

        return cls._instance


__monster_db = MonsterDB()

get_info_by_ID = __monster_db.get_info_by_ID
