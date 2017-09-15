# coding=utf-8
data = {
    'start': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['attack02'],
        'next': {
            'tag': {
				'mov': ['mov_1'],
                'hit': ['hit_1'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 1.4,  # 攻击百分比
            'add': 0,  # 攻击附加
            'sector': [240, 160],  # 有此项表示扇形区域攻击，参数1:扇形半径, 参数2:扇形角度
        },
        "sfx": [["/fx/other/hited_light.sfx", 8.0, 'hit']],
        'face': True,
        'hitact': 'hit',
    },
	
	'mov_1': {
        'type': 'move',
        'args': [0, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 400,
    },
}
