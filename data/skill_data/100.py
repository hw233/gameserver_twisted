# coding=utf-8
data = {
    'start': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['collect'],
        'next': {
            'tag': {
                'hit': ['hit_1'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 50.0,  # 攻击百分比
            'add': 0,  # 攻击附加
            'single': True,  # 采集
        },
    },

}
