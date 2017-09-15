# coding=utf-8
data = {
    'start': ['act1'],

    'act1': {
        'type': 'act',
        'end': True,
        'args': ['throw_ready'],
        'next': {
            'tag': {
                'holdforce': ['holdforce'],
            },
        },
    },

    'holdforce': {
        'type': 'holdforce',
        'hold_idle': 'throw_idle',
        'hold_run': 'throw_walk',
        'loop': True,
        'looptime': 1.0,
        'speed_percentage': 0.5,
        'arrive_percentage': 0.8,
        'arrive_stage': 'act2',
        'not_arrive_stage': 'act3',
    },

    'act2': {
        'type': 'act',
        'end': True,
        'args': ['throw_attack'],
        'next': {
            'tag': {
                'hit': ['hit_1'],
                'mov': ['mov_1'],
            },
        },
    },

    'hit_1': {
        'type': 'att',
        'damage': {
            'percentage': 2,  # 攻击百分比
            'add': 0,  # 攻击附加
            'stop': 6,
            'quake': [1, 6, 2],
            'shake': [1, 4],
            'bullet': {
                'speed': 3000,  # 初始速度
                'acceleration': 1500,  # 加速度
                'max_dis': 1300,  # 子弹最大飞行距离
                'col_radius': 1,  # 子弹球体碰撞体半径
                'fly_sfx': ['fx/other/lance_feixing.sfx', 5.0, 'bullet_point'],  # 飞行特效
            },
        },
        'sfx': [["fx/other/lance_jidao.sfx", 5.0, 'hit']],
        'face': True,
        'blowdown': -1200,
    },

    'mov_1': {
        'type': 'move',
        'args': [0, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 1300,
    },

    'act3': {
        'type': 'act',
        'end': True,
        'args': ['throw_attack'],
        'next': {
            'tag': {
                'hit': ['hit_2'],
                'mov': ['mov_2'],
            },
        },
    },

    'hit_2': {
        'type': 'att',
        'damage': {
            'percentage': 1,  # 攻击百分比
            'add': 0,  # 攻击附加
            'shake': [1, 2],
            'bullet': {
                'speed': 2000,  # 初始速度
                'acceleration': 1000,  # 加速度
                'max_dis': 800,  # 子弹最大飞行距离
                'col_radius': 1,  # 子弹球体碰撞体半径
                'fly_sfx': ['fx/other/lance_feixing.sfx', 5.0, 'bullet_point'],  # 飞行特效
            },
        },
        'sfx': [["fx/other/lance_canliu.sfx", 5.0, 'hit']],
        'hitact': 'hit',
        'face': False,
    },

    'mov_2': {
        'type': 'move',
        'args': [0, 0],  # 产生速度: XZ速度，速度添加的持续时间
        'faceto': 800,
    },

}
