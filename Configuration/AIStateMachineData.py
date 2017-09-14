# coding=utf-8
data = {
    # 不写状态转移为0，即可以进入状态
    # 1 为不可进入状态
    'idle': {
        'id': 1,
        'father': True,
    },

    'run': {
        'id': 2,
        'father': True,
    },

    'atk': {
        'id': 3,
        'father': True,
        'idle': 1,
        'run': 1,
        'defence': 1,
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
        'id': 6,
        'father': True,
        'idle': 1,
        'run': 1,
        'atk': 1,
        'defence': 1,
        'holdforce': 2,
        'holdforce_single': 2,
        'stiffness': 1,
        'liedown': 1,
        'buff': 1,
        'no_move': 1,
    },

    'dead': {
        'id': 7,
        'father': True,
        'idle': 1,
        'run': 1,
        'atk': 1,
        'defence': 1,
        'holdforce_single': 1,
        'holdforce': 1,
        'stiffness': 1,
        'liedown': 1,
        'dead': 1,
        'block': 1,  # 碰撞
        'no_move': 1,  # 不可位移
        'no_atk': 1,  # 不可受到伤害
        'buff': 1,
    },
}
