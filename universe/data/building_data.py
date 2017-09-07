left_top = [
    # [
    #     {
    #         'comp': 'renderer',
    #         'gim': 'scene/town/town_01.gim'
    #     },
    #     {
    #         "comp": "collider",
    #         "type": "AABB",
    #         "static": True,
    #         "shape": {
    #             "width": 400,
    #             "height": 300,
    #             "length": 100,
    #         },
    #         "center": {
    #             "x": 200, "y": 150, "z": 0
    #         },
    #         "outline_visible": True
    #     },
    # ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_05.gim'
        },
        {
            "comp": "collider",
            "type": "AABB",
            "static": True,
            "shape": {
                "width": 100,
                "height": 300,
                "length": 400,
            },
            "center": {
                "x": 0, "y": 150, "z": -200
            },
            "outline_visible": True
        },
        {
            "comp": "collider",
            "type": "AABB",
            "static": True,
            "shape": {
                "width": 300,
                "height": 300,
                "length": 100,
            },
            "center": {
                "x": 100, "y": 150, "z": 0
            },
            "outline_visible": True
        },
    ],
    # [
    #     {
    #         'comp': 'renderer',
    #         'gim': 'scene/town/town_09.gim'
    #     },
    # ],
    # [
    #     {
    #         'comp': 'renderer',
    #         'gim': 'scene/town/town_10.gim'
    #     },
    #
    # ],
]

right_top = [
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_02.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_06.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_09.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_10.gim'
        }
    ],
]

left_bottom = [
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_03.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_07.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_09.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_10.gim'
        }
    ],
]
right_bottom = [
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_04.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_08.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_09.gim'
        }
    ],
    [
        {
            'comp': 'renderer',
            'gim': 'scene/town/town_10.gim'
        }
    ],
]

data = {
    'left_top': left_top, 0: left_top,
    'right_top': right_top, 1: right_top,
    'left_bottom': left_bottom, 2: left_bottom,
    'right_bottom': right_bottom, 3: right_bottom
}