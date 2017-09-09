# coding=utf-8

#单人模式
single_model = [
    {#stage 1
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID 怪物种类
                "total_num": 2, #怪物总数
                "interval_time": 10, #刷新间隔时间
                "first_random_num" : [2,4], #第一次刷新数量范围
                "next_random_num" : [2,5] #以后每一波刷新数量范围
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    },
    {#stage 2
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    }
]

#生存模式
normal_model = [
    {#stage 1
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    },
    {#stage 2
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    }
]

#合作模式
battle_model = [
    {#stage 1
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    },
    {#stage 2
        "stage_time" : 150, # 距离上一波野怪刷新的时间
        "remind_time" : 60, # 客户端提示时间
        "alert_time" : 30, # 红色文字提示时间
        "monster_setting" : [
            {
                "ID" : 100, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            },
            {
                "ID" : 101, # monster ID
                "total_num": 2,
                "interval_time": 10,
                "first_random_num" : [2,4],
                "next_random_num" : [2,5]
            }
        ]
    }
]