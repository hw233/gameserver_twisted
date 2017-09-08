# coding=utf-8
data = {
    'start': ['act1', 'act2', 'act3'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack01'],
        'next': {
            'tag': {
                'hit': ['hit_1'],
            },
        },
    },

    'act2': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack02'],
        'next': {
            'tag': {
                'hit': ['hit_2'],
                'mov': ['mov_2'],
            },
        },
    },

    'act3': {
        'type': 'act',
        'end': True,
        'args': ['hammer_attack03'],
        'next': {
            'tag': {
                'hit_01': ['hit_3'],
                'hit_02': ['hit_3'],
                'hit_03': ['hit_3'],
                'hit_04': ['hit_3'],
                'hit_05': ['hit_4'],
                'mov': ['mov_3'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [180, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-200, 1],
        "sfx": [["/fx/other/hited_light.sfx", 9.0, 'hit']],
        'stop': 4,
        'quake': [0.5, 4, 2],
        'face': True,
        'hitact': 'hit',
        # 'hitime': 0.1,
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [180, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-300, 1],
        'quake': [0.3, 2, 2],
        "sfx": [["/fx/other/hited_light.sfx", 9.0, 'hit']],
        'face': True,
        'stop': 2,
        'hitact': 'hit02',
    },

    'hit_3': {
        'type': 'att',
        'damage': {
            'percentage': 0.2,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_heavy.sfx", 5.0, 'hit']],
        'face': True,
        'hitact': 'hit',
    },

    'hit_4': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 180],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-1000, 1],
        "sfx": [["/fx/other/hited_heavy.sfx", 5.0, 'hit']],
        'face': True,
        'quake': [0.6, 4, 2],
        'shake': [0, 5],
        'stop': 4,
        # 'hitact': 'hit',
        'blowdown': -1500,
    },

    # 'mov_1': {
    #     'type': 'move',
    #     'args': [1400, 0],  # 产生速度: XZ速度，速度添加的持续时间
    #     'faceto': 300,
    # },

    'mov_2': {
        'type': 'move',
        'args': [300, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },

    'mov_3': {
        'type': 'move',
        'args': [500, 0.4],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },
}
