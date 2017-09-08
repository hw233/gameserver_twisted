# coding=utf-8
data = {
    'start': ['act1', 'act2'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['quanji'],
        'next': {
            'tag': {
                'hit': ['hit_1'],
                'mov': ['mov_1'],
            },
        },
    },

    'act2': {
        'type': 'act',
        'end': True,
        'args': ['quanji02'],
        'next': {
            'tag': {
                'hit': ['hit_2'],
                'mov': ['mov_2'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-700, 1],
        'stop': 2,
        'quake': [0.6, 2, 2],
        "sfx": [["/fx/other/hited_light.sfx", 8.0, 'hit']],
        'face': True,
        'hitact': 'hit',
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [210, 120],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        'move': [-1400, 1],
        'quake': [0.8, 4, 2],
        'face': True,
        'stop': 4,
        "sfx": [["/fx/other/hited_light.sfx", 8.0, 'hit']],
        'hitact': 'hit02',
    },

    'mov_1': {
        'type': 'move',
        'args': [800, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },

    'mov_2': {
        'type': 'move',
        'args': [700, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 300,
    },
}
