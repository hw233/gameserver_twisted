# coding=utf-8
data = {
    'start': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['collect_kan'],
        'next': {
            'tag': {
                'holdforce_single': ['holdforce_single_1']
            },
        },
    },

    'holdforce_single_1': {  # 用于单动作静止蓄力
        'type': 'holdforce_single',
        'loop': False,
        'looptime': 2.0,
        'arrive_percentage': 0.8,
        # 蓄力成功播放事件事件
        'arrive_stage': {
            'hit': ['hit_1']
        },
        # 蓄力失败播放事件事件
        'not_arrive_stage': {
            'hit': ['hit_2']
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 5.0,  # 攻击百分比
            'single': True,
        },
        # 'stop': 3,
        # 'quake': [0.4, 2 ,2],
        'hitact': 'hit',
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 1.0,  # 攻击百分比
            'single': True,
        },
        # 'stop': 3,
        # 'quake': [0.4, 2 ,2],
        'hitact': 'hit',
    },

}
