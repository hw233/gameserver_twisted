monster_01 = [
    {
        'comp': 'transform',
    },
    {
        'comp': 'renderer',
        'gim': 'model/monster/monster01.gim'
    },
    {
        'comp': 'animator',
        'animations #animator': 'monster_01'
    },
    {
        'comp': 'monster',
        'move_speed': 200,
        'attack_speed': 200,
        'attack_range': 300,
        'detection_range': 3000
    },
    {
        'comp': 'collider',
        'colliders': [
            {
                'type': 'AABB',
                'shape': {
                    'width': 100, 'height': 100, 'length': 100
                },
                'center': {
                    'x': 0, 'y': 50, 'z': 0
                }
            }
        ]
    },
    {
        'comp': 'state',
        'default': 'idle',
        'states': ['idle', 'walk', 'hit', 'attack'],
        'transitions': {
            'idle': {
                'walk': 'walk',
                'hit': 'hit',
                'attack': 'attack'
            },
            'walk': {
                'idle': 'idle',
                'hit': 'hit',
                'attack': 'attack'
            },
            'hit': {
                'idle': 'idle',
                'walk': 'walk'
            },
            'attack': {
                'idle': 'idle',
                'walk': 'walk',
                'hit': 'hit',
            }
        }
    }
]


data = {
    'monster_01': monster_01, 1: monster_01
}