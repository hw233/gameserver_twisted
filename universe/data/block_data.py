# coding=utf-8

AMOUNT_0 = (0)
AMOUNT_1 = (0.005, 0.008)
AMOUNT_2 = (0.008, 0.01)
AMOUNT_3 = (0.01, 0.02)
AMOUNT_4 = (0.02, 0.03)
AMOUNT_5 = (0.03, 0.04)
AMOUNT_6 = (0.04, 0.05)
AMOUNT_7 = (0.05, 0.06)
AMOUNT_8 = (0.06, 0.07)
AMOUNT_9 = (0.07, 0.08)
AMOUNT_10 = (0.08, 0.10)

block_town = {
    # 城镇区
    "id": 1,
    "name": "town",
    "area @rand.int": (1000, 2000),
    "landform #landform": "mud",
    "sockets": [2, 3, 4],
    "buildings": {
        'amount @rand.float': (0.02, 0.05),
    },
    "spots": {
        "spot #spot": "adobe",
        "amount @rand.float": (0.3, 0.4),
    },
    "biomes": [
        {
            # 资源树
            "item #item": "tree",
            "amount @rand.float": AMOUNT_2,
            "density": 0.8,
        },
		{
            # 资源黄色的树
            "item #item": "yellow_tree",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
		{
			# 资源枯树
            "item #item": "y_withered_tree",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
            # 资源树枝
            "item #item": "branch",
            "amount @rand.float": AMOUNT_2,
            "density": 0.4,
        },
		{
            # 资源草
            "item #item": "y_reed",
            "amount @rand.float": AMOUNT_2,
            "density": 0.8,
        },
		{
            # 资源浆果
            "item #item": "berry",
            "amount @rand.float": AMOUNT_2,
            "density": 0.8,
        },
		{
            # 资源鸟蛋
            "item #item": "egg",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
		{
            # 资源石头
            "item #item": "stone04",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
		{
			# 普通物品树桩
            "item #item": "stump",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
		{
			# 普通物品黄色小草
            "item #item": "yellow_weeds",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
		{
			# 普通物品小草
            "item #item": "p_weeds",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
        {
			# 普通物品草丛
            "item #item": "p_bush",
            "amount @rand.float": AMOUNT_1,
            "density": 0.8,
        },
		{
			# 普通物品黄色草丛
            "item #item": "y_bush",
            "amount @rand.float": AMOUNT_2,
            "density": 0.8,
        },
		{
			# 普通物品小石块1
            "item #item": "stone01",
            "amount @rand.float": AMOUNT_7,
            "density": 0.2,
        },
		{
			# 普通物品，小罐子
            "item #item": "jar",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
		{
			# 普通物品，小桶
            "item #item": "cask",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
		{
			# 普通物品，小巷子
            "item #item": "box01",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
    ],
}

block_grass = {
    # 草地区
    "id": 2,
    "name": "grass",
    "area @rand.int": (1000, 1500),
    "landform #landform": "grass",
    "sockets": [1],
    "spots": {
        "spot #spot": "soil",
        "amount @rand.float": (0.2, 0.3),
    },
    "biomes": [
        {
			# 普通物品草丛
            "item #item": "p_bush",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
        {
            # 资源树
            "item #item": "tree",
            "amount @rand.float": AMOUNT_8,
            "density": 0.8,
        },
        {
            # 资源黄色的树
            "item #item": "yellow_tree",
            "amount @rand.float": AMOUNT_8,
            "density": 0.8,
        },
        {
			# 资源枯树
            "item #item": "withered_tree",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
        {
            # 资源树枝
            "item #item": "branch",
            "amount @rand.float": AMOUNT_5,
            "density": 0.4,
        },
        {
            # 资源草
            "item #item": "reed",
            "amount @rand.float": AMOUNT_6,
            "density": 0.8,
        },
        {
            # 资源浆果
            "item #item": "berry",
            "amount @rand.float": AMOUNT_7,
            "density": 0.8,
        },
        {
            # 资源鸟蛋
            "item #item": "egg",
            "amount @rand.float": AMOUNT_2,
            "density": 0.2,
        },
        {
            # 资源石头
            "item #item": "stone04",
            "amount @rand.float": AMOUNT_5,
            "density": 0.2,
        },
        {
			# 普通物品树桩
            "item #item": "stump",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
        {
			# 普通物品黄色小草
            "item #item": "yellow_weeds",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
        {
			# 普通物品小草
            "item #item": "p_weeds",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
        {
			# 普通物品小石块1
            "item #item": "stone01",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
        {
			# 普通物品，小罐子
            "item #item": "jar",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
        {
			# 普通物品，小桶
            "item #item": "cask",
            "amount @rand.float": AMOUNT_2,
            "density": 0.2,
        },
        {
			# 普通物品，小巷子
            "item #item": "box01",
            "amount @rand.float": AMOUNT_3,
            "density": 0.2,
        },
    ],
}

block_withered = {
    # 枯草地
    "id": 3,
    "name": "withered",
    "area @rand.int": (1000, 1500),
    "landform #landform": "withered",
    "sockets": [1],
    "spots": {
        "spot #spot": "barren",
        "amount @rand.float": (0.2, 0.3),
    },
    "biomes": [
	    {
            # 资源树
            "item #item": "tree",
            "amount @rand.float": AMOUNT_1,
            "density": 0.8,
        },
		{
            # 资源黄色的树
            "item #item": "yellow_tree",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
		{
			# 资源枯树
            "item #item": "withered_tree",
            "amount @rand.float": AMOUNT_7,
            "density": 0.2,
        },
		{
            # 资源树枝
            "item #item": "branch",
            "amount @rand.float": AMOUNT_5,
            "density": 0.4,
        },
		{
            # 资源草
            "item #item": "y_reed",
            "amount @rand.float": AMOUNT_7,
            "density": 0.8,
        },
		{
            # 资源浆果
            "item #item": "berry",
            "amount @rand.float": AMOUNT_1,
            "density": 0.8,
        },
		{
            # 资源鸟蛋
            "item #item": "egg",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
            # 资源石头
            "item #item": "stone04",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
		{
			# 普通物品树桩
            "item #item": "stump",
            "amount @rand.float": AMOUNT_4,
            "density": 0.2,
        },
		{
			# 普通物品黄色小草
            "item #item": "yellow_weeds",
            "amount @rand.float": AMOUNT_7,
            "density": 0.2,
        },
		{
			# 普通物品小草
            "item #item": "p_weeds",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
        {
			# 普通物品草丛
            "item #item": "y_bush",
            "amount @rand.float": AMOUNT_3,
            "density": 0.8,
        },
		{
			# 普通物品小石块1
            "item #item": "stone01",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
			# 普通物品，小罐子
            "item #item": "jar",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
			# 普通物品，小桶
            "item #item": "cask",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
			# 普通物品，小巷子
            "item #item": "box01",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
    ],
}

block_marsh = {
    # 沼泽
    "id": 4,
    "name": "marsh",
    "area @rand.int": (1000, 1500),
    "landform #landform": "marsh",
    "sockets": [1],
    "spots": {
        "spot #spot": "puddle",
        "amount @rand.float": (0.3, 0.4),
    },
    "biomes": [
	    {
            # 资源树
            "item #item": "tree",
            "amount @rand.float": AMOUNT_1,
            "density": 0.8,
        },
		{
            # 资源黄色的树
            "item #item": "yellow_tree",
            "amount @rand.float": AMOUNT_1,
            "density": 0.8,
        },
		{
			# 资源枯树
            "item #item": "y_withered_tree",
            "amount @rand.float": AMOUNT_8,
            "density": 0.2,
        },
		{
            # 资源树枝
            "item #item": "branch",
            "amount @rand.float": AMOUNT_4,
            "density": 0.4,
        },
		{
            # 资源草
            "item #item": "y_reed",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
		{
            # 资源浆果
            "item #item": "berry",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
		{
            # 资源鸟蛋
            "item #item": "egg",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
		{
            # 资源石头
            "item #item": "stone04",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
		{
			# 普通物品树桩
            "item #item": "stump",
            "amount @rand.float": AMOUNT_5,
            "density": 0.2,
        },
		{
			# 普通物品P小草
            "item #item": "p_weeds",
            "amount @rand.float": AMOUNT_7,
            "density": 0.2,
        },
		{
			# 普通物品黄色小草
            "item #item": "yellow_weeds",
            "amount @rand.float": AMOUNT_2,
            "density": 0.2,
        },
        {
			# 普通物品草丛
            "item #item": "p_bush",
            "amount @rand.float": AMOUNT_5,
            "density": 0.8,
        },
		{
			# 普通物品小石块1
            "item #item": "stone01",
            "amount @rand.float": AMOUNT_6,
            "density": 0.2,
        },
		{
			# 普通物品，小罐子
            "item #item": "jar",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
			# 普通物品，小桶
            "item #item": "cask",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
		{
			# 普通物品，小巷子
            "item #item": "box01",
            "amount @rand.float": AMOUNT_1,
            "density": 0.2,
        },
	
    ],
}

data = [
    block_town,
    block_grass,
    block_withered,
    block_marsh
]
