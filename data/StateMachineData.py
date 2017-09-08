# coding=utf-8
data = {
    # 不写状态转移为0，即可以进入状态
    # 1 为不可进入状态
    'idle': {
        'id': 1,
        'father': True,
        'ani': {
            'all': 'idle',
            '2000': 'idle',
        },
    },

    'run': {
        'id': 2,
        'father': True,
        'ani': {
            'all': 'run',
            '2001': 'run_weapon',
            '2002': 'run_weapon',
            '2003': 'run_weapon',
            '2004': 'run_weapon',
        },
    },

    'atk': {
        'id': 3,
        'father': True,
        'idle': 1,
        'run': 1,
        'defence': 1,
    },

    'defence': {
        'id': 4,
        'stiffness': 1,
        'defence': 1,
        'liedown': 1,
        'buff': 1,
        'atk': 2,  # 2 表示可以进入该父状态，删除自己
        'change': {  # 蓄力状态改变idle和run动作
            'idle': 'idle_guard',
            'run': 'walk_guard',
            'speed_percentage': 0.3,
        },
    },

    'stiffness': {
        'id': 5,
        'father': True,
        'idle': 1,
        'run': 1,
        'atk': 1,
        'defence': 1,
    },

    'liedown': {
        'ani': {
            'all': 'fall02',
        },
        'up_ani': {
            'all': 'up',
        },
        'id': 6,
        'father': True,
        'idle': 1,
        'run': 1,
        'atk': 1,
        'defence': 1,
        'stiffness': 1,
        'liedown': 1,
        'buff': 1,
        # 'block': 1,
        'no_move': 1,
    },

    'dead': {
        'ani': {
            'all': 'fall02',
        },
        'id': 7,
        'father': True,
        'idle': 1,
        'run': 1,
        'atk': 1,
        'defence': 1,
        'stiffness': 1,
        'liedown': 1,
        'dead': 1,
        'block': 1,  # 碰撞
        'no_move': 1,  # 不可位移
        'no_atk': 1,  # 不可受到伤害
        'buff': 1,
    },

    'bati': {
        'id': 8,
        'stiffness': 1,
        'liedown': 1,
        'no_move': 1,  # 不可位移
        'buff': 1,
    },

    'holdforce': {
        'id': 9,
        'stiffness': 1,
        'defence': 1,
    },

    'holdforce_single': {
        'id': 10,
        'stiffness': 1,
        'defence': 1,
        'idle': 1,
        'run': 1,
        'atk': 1,
    },

    'god': {
        'id': 11,
        'stiffness': 1,
        'liedown': 1,
        'no_atk': 1,
        'no_move': 1,  # 不可位移
        'buff': 1,
    },
}
