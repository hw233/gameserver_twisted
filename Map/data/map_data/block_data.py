# coding=utf-8

data = [
    {
        # 草地区
        "id": 2,
        "name": "grass",
        "center @grid.position": (-15, 15),
        "area @rand.int": (500, 700),
        "landform #landform": "grass",
        "holes": {
            "area @rand.int": (10, 30)
        },
        "spots": [
            {
                "spot #spot": "soil",
                "proportion @rand.float": (0.10, 0.20)
            }
        ],
        "biomes": [
            {
                "item #item": "tree",
                "proportion @rand.float": (0.05, 0.10),
                "density": 0.8,
                "associated": [
                    {
                        "item #item": "dead_tree",
                        "proportion @rand.float": (0, 0.01),
                        "density": 0.4,
                    }
                ]
            },
            {
                "item #item": "withered_tree",
                "proportion @rand.float": (0.03, 0.05),
                "density": 0.8,
            },
            {
                "item #item": "reed",
                "proportion @rand.float": (0.05, 0.2),
                "density": 0.8,
            },
            {
                "item #item": "bush",
                "proportion @rand.float": (0.05, 0.08),
                "density": 0.8,
            },
            {
                "item #item": "stump",
                "proportion @rand.float": (0.01, 0.03),
                "density": 0.8,
            },
            {
                "item #item": "berry",
                "proportion @rand.float": (0.1, 0.15),
                "density": 0.8,
            }
        ],
    },
]
