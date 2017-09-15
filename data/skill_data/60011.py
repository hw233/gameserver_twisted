# coding=utf-8
data = {
    'start': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['eat'],
        'next': {
            'tag': {
                'holdforce_single': ['holdforce_single_1']
            },
        },
    },

    'holdforce_single_1': {  # 用于单动作静止蓄力
        'type': 'holdforce_single',
        'loop': False,
        'looptime': 0.5,
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
            'blood_percentage': 2.25,  # 对单体有效 'blood' 为治疗自身血量, single为true的时候才可以填写
            'power_percentage': 1.5,  # 'power' 为提高提高自身体力 所有属性以攻击力为准, single为true的时候才可以填写
            'single': True,

        },
        # 'stop': 3,
        # 'quake': [0.4, 2 ,2],
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'blood_percentage': 1.5,
            'power_percentage': 1,
            'single': True,
        },
        # 'stop': 3,
        # 'quake': [0.4, 2 ,2],
    },

}
