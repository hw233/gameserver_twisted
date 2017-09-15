# coding=utf-8

#单人模式
single_model = {
    "map_monster":[
        {
			# 刷新铁怪
            "ID": 100,
            "total_num": 5,
            "refresh_location": "town"
        },
		{
			# 刷新兔子
            "ID": 201,
            "total_num": 7,
            "refresh_location": "withered"
        },
    ],
    "win_time" : 800, # 获胜时间
    "win_remind_time": 120, #获胜倒计时
    "first_stage_time" : [180, 180], #第一波野怪刷新时间
    "next_stage_time" : [120, 120], # 距离上一波野怪刷新的时间
    "alert_time" : 30, # 红色文字提示时间
    "interval_time": [8, 10],  # 刷新间隔时间
    "first_random_num": [2, 4],  # 第一次刷新数量范围
    "next_random_num": [2, 5],  # 以后每一波刷新数量范围
    "monster_setting" : [
        {
            "ID" : 101, # monster ID 怪物种类
            "total_num": [1, 1, 2, 2, 2], #怪物总数
        },
        {
            "ID" : 102, # monster ID
            "total_num": [0, 1, 1, 1, 1], #怪物总数
        },
		{
            "ID" : 103, # monster ID
            "total_num": [0, 0, 0, 0, 1], #怪物总数
        }
    ]
}

#生存模式
normal_model = {
    "map_monster": [
        {
			# 刷新铁怪
            "ID": 100,
            "total_num": 13,
            "refresh_location": "town"
        },
		{
			# 刷新兔子
            "ID": 201,
            "total_num": 20,
            "refresh_location": "withered"
        },
    ],
    "win_time" : 800, # 获胜时间
    "win_remind_time": 120, #获胜倒计时
    "first_stage_time" : [180, 180], #第一波野怪刷新时间
    "next_stage_time" : [120, 120], # 距离上一波野怪刷新的时间
    "alert_time" : 30, # 红色文字提示时间
    "interval_time": [8, 10],  # 刷新间隔时间
    "first_random_num": [2, 4],  # 第一次刷新数量范围
    "next_random_num": [2, 5],  # 以后每一波刷新数量范围
    "monster_setting": [
        {
            "ID": 101,  # monster ID 怪物种类
            "total_num": [1, 1, 2, 2, 2],  # 怪物总数
        },
        {
            "ID": 102,  # monster ID
            "total_num": [0, 1, 1, 2, 2],  # 怪物总数
        },
		{
            "ID" : 103, # monster ID
            "total_num": [0, 0, 0, 0, 1], #怪物总数
        }
    ]
}

#合作模式
battle_model = {
    "map_monster":[
        {
			# 刷新铁怪
            "ID": 100,
            "total_num": 11,
            "refresh_location": "town"
        },
		{
			# 刷新兔子
            "ID": 201,
            "total_num": 15,
            "refresh_location": "withered"
        },
    ],
    "win_time" : 800, # 获胜时间
    "win_remind_time": 120, #获胜倒计时
    "first_stage_time" : [180, 180], #第一波野怪刷新时间
    "next_stage_time" : [120, 120], # 距离上一波野怪刷新的时间
    "alert_time" : 30, # 红色文字提示时间
    "interval_time": [8, 10],  # 刷新间隔时间
    "first_random_num": [2, 4],  # 第一次刷新数量范围
    "next_random_num": [2, 5],  # 以后每一波刷新数量范围
    "monster_setting": [
        {
            "ID": 101,  # monster ID 怪物种类
            "total_num": [2, 3, 4, 5, 6],  # 怪物总数
        },
        {
            "ID": 102,  # monster ID
            "total_num": [0, 2, 2, 3, 3],  # 怪物总数
        },
		{
            "ID" : 103, # monster ID
            "total_num": [0, 0, 0, 0, 1], #怪物总数
        }
    ]
}