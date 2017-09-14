# coding=utf-8
data = {

    # 地块大小
    'tile': {
        'width': 200,
        'length': 200
    },

    # 单块建筑大小
    'building': {
        'horizontal': 4,
        'vertical': 4,
        'margin': 1,
    },

    "biomes": {
        "cluster": (3, 5),
        "rotation": (-60, 60)
    },

    'player': {
        'components': [
            {
                'comp': 'transform'
            },
            { 'comp': 'player' }
        ]
    },

    # 层
    # :param name: 层名称
    # :param altitude: 海拔高度
    # :param preset: 预设物体
    'layers': {
        'ocean': {
            'altitude': -350,
            'presets': [
                [{
                    'comp': 'transform',
                    'position': {
                        'x': 0,
                        'y': -350,
                        'z': 0
                    }
                },
                {
                    'comp': 'renderer',
                    'gim': 'scene/water/water.gim',
                }]
            ]
        },
        'terrain': {
            'altitude': -8,
            'presets': []
        },
        'building': {
            'altitude': -8,
            'presets': []
        },
        'biont': {
            'altitude': -2,
            'presets': []
        },
        'drop': {
            'altitude': -2,
            'presets': []
        },
        'monster': {
            'altitude': 0,
            'presets': []
        },
        'player': {
            'altitude': 0,
            'presets': []
        }
   },


    'debug': {
        'grid': {
            'visible': False
        },

        'collision': {
            'outline': {
                'visible': True
            }
        },
    }
}
