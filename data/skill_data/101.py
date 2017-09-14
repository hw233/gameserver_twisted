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
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'single': True,
        },
        'hitact': 'hit',
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'single': True,
        },
        'hitact': 'hit',
    },

}
