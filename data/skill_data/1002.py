# coding=utf-8
data = {
    'start': ['act0'],

    'act0': {
        'type': 'act',
        'end': True,
        'args': ['hammer_ready'],
        'next': {
            'tag': {
                'holdforce': ['holdforce']
            },
        },
    },

    'holdforce': {
        'type': 'holdforce',
        'hold_idle': 'hammer_ready_idle',
        'hold_run': 'hammer_ready_run',
        'loop': False,
        'looptime': 3.0,
        'speed_percentage': 0.66,
        'arrive_percentage': 0.8,
        'arrive_stage': 'start1',
        'not_arrive_stage': 'start2',
    },

    # --------------------------------
    'start1': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack03'],
        'next': {
            'tag': {
                'mov': ['mov_1'],
                'hit_01': ['hit_1'],
                'hit_02': ['hit_2'],
                'hit_03': ['hit_1'],
                'hit_04': ['hit_2'],
                'hit_05': ['hit_1'],
                'hit_06': ['hit_2'],
                'hit_07': ['hit_1'],
                'hit_08': ['hit_3'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 0.25,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_light.sfx", 5.0, 'hit']],
        'face': True,
        'hitact': 'hit',
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 0.25,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_light.sfx", 5.0, 'hit']],
        'face': True,
        'hitact': 'hit02',
    },

    'hit_3': {
        'type': 'att',
        'damage': {
            'percentage': 1.25,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_heavy.sfx", 5.0, 'hit']],
        'face': True,
        'quake': [1, 6, 2],
        'shake': [0, 5],
        'stop': 6,
        # 'hitact': 'hit',
        'blowdown': -1500,
    },

    'mov_1': {
        'type': 'move',
        'args': [2100, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 500,
    },

    # -------------------------------------------------------------------

    'start2': ['act11', 'act12', 'act13'],

    'act11': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack01'],
        'next': {
            'tag': {
                'mov': ['mov_11'],
                'hit': ['hit_11'],
            },
        },
    },

    'act12': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack02'],
        'next': {
            'tag': {
                'mov': ['mov_12'],
                'hit': ['hit_12'],
            },
        },
    },

    'act13': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack_0301'],
        'next': {
            'tag': {
                'mov': ['mov_13'],
                'hit': ['hit_13'],
            },
        },
    },

    'hit_11': {
        'type': 'att',
        'damage': {
            'percentage': 0.4333,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [180, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-800, 1],
        "sfx": [["/fx/other/hited_light.sfx", 9.0, 'hit']],
        'stop': 4,
        'quake': [0.5, 4, 2],
        'face': True,
        'hitact': 'hit',
        # 'hitime': 0.1,
    },

    'hit_12': {
        'type': 'att',
        'damage': {
            'percentage': 0.4,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [180, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-600, 1],
        'quake': [0.3, 2, 2],
        "sfx": [["/fx/other/hited_light.sfx", 9.0, 'hit']],
        'face': True,
        'stop': 2,
        'hitact': 'hit02',
    },

    'hit_13': {
        'type': 'att',
        'damage': {
            'percentage': 0.733,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_heavy.sfx", 5.0, 'hit']],
        'face': True,
        'quake': [0.6, 4, 2],
        'shake': [0, 5],
        'stop': 4,
        'hitact': 'hit',
        'move': [-1400, 1],
    },

    'mov_11': {
        'type': 'move',
        'args': [1000, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },

    'mov_12': {
        'type': 'move',
        'args': [800, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },

    'mov_13': {
        'type': 'move',
        'args': [600, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },

}
