# coding=utf-8

block_town = {
    # 城镇区
    "id": 1,
    "name": "town",
    "center": (0, 0),
    "area @rand.int": (1000, 1500),
    "landform #landform": "mud",
    "buildings": {
        'proportion @rand.float': (0.02, 0.05),
    },
    "spots": {
        "spot #spot": "adobe",
        "proportion @rand.float": (0.3, 0.4),
    },
    "biomes": [
        {
            # 资源树
            "item #item": "tree",
            "proportion @rand.float": (0.005, 0.01),
            "density": 0.8,
        },
        {
            "item #item": "stone01",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "stone02",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "box01",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "stump",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "weeds",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "jar",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "cask",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            # 资源树枝
            "item #item": "branch",
            "proportion @rand.float": (0.03, 0.08),
            "density": 0.4,
        },
		{
            # 资源草
            "item #item": "reed",
            "proportion @rand.float": (0.005, 0.02),
            "density": 0.8,
        },
		{
            # 浆果
            "item #item": "berry",
            "proportion @rand.float": (0, 0.000001),
            "density": 0.8,
        },
		{
            # 资源鸟蛋
            "item #item": "egg",
            "proportion @rand.float": (0.005, 0.01),
            "density": 0.2,
        },
		{
            # 石头
            "item #item": "stone04",
            "proportion @rand.float": (0.03, 0.08),
            "density": 0.2,
        },
    ],
}

block_grass = {
    # 草地区
    "id": 2,
    "name": "grass",
    "center": (-20, 20),
    "area @rand.int": (500, 700),
    "landform #landform": "grass",
    "holes": {
        "area @rand.int": (10, 30)
    },
    "spots": {
        "spot #spot": "soil",
        "proportion @rand.float": (0.2, 0.3),
    },
    "biomes": [
        {
            # 资源树
            "item #item": "tree",
            "proportion @rand.float": (0.15, 0.2),
            "density": 0.8,
        },
        {
            "item #item": "branch",             #资源树枝
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.4,
        },
		{
            "item #item": "reed",               #资源草
            "proportion @rand.float": (0.02, 0.05),
            "density": 0.8,
        },
		{
            "item #item": "berry",        #浆果
            "proportion @rand.float": (0.05, 0.15),
            "density": 0.8,
        },
		{
            "item #item": "egg",          #资源鸟蛋
            "proportion @rand.float": (0, 0.00001),
            "density": 0.2,
        },
		{
            "item #item": "stone04",       #石头
            "proportion @rand.float": (0.005, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "withered_tree",
            "proportion @rand.float": (0.02, 0.03),
            "density": 0.2,
        },
        {
            "item #item": "bush",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.8,
        },
        {
            "item #item": "stump",
            "proportion @rand.float": (0.01, 0.03),
            "density": 0.8,
        },

        {
            "item #item": "stone01",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
        {
            "item #item": "rabbit",
            "proportion @rand.float": (0.01, 0.02),
            "density": 0.2,
        },
    ],
}

block_withered = {
    # 枯草地
    "id": 3,
    "name": "withered",
    "center": (0, -15),
    "area @rand.int": (500, 700),
    "landform #landform": "withered",
    "spots": {},
    "biomes": [
    ],
}

block_marsh = {
    # 沼泽
    "id": 4,
    "name": "marsh",
    "center": (15, 15),
    "area @rand.int": (500, 700),
    "landform #landform": "marsh",
    "spots": {},
    "biomes": [
    ],
}

data = [
    block_town,
    block_grass,
    # block_withered,
    # block_marsh
]
