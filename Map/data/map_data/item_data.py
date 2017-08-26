# coding=utf-8

'''
结构说明:
    id 种类id
    name 种类名称
	type 类型 unit需要攻击, good可直接拾取, none不可交互
    collision 碰撞盒
    dead 死亡之后对应的物品，当类型为unit时，采集死亡后，留下来的物件名称
	dropgood 物件死亡之后，掉落的物品
	good_id 当类型为goods时，填写为物品ID
'''

item_berry = {          #浆果
    "id": 1,
    "name": "berry",
	"type": "unit",
    "width": 0.75,
    "height": 0.75,
    "gim": "model/berry/berry.gim",
	"dead #item": "dead_berry",
	"drop_good": 6001,
	"collect_time":1,
}

item_dead_berry = {          #浆果死亡
    "id": 2,
    "name": "dead_berry",
	"type": "none",
    "width": 0.75,
    "height": 0.75,
    "gim": "model/berry/dead_berry.gim",
}

item_bush = {              #大草
    "id": 3,
    "name": "bush",
	"type": "none",
    "width": 3,
    "height": 2.5,
    "gim": "model/bush/bush.gim"
}

item_dead_tree = {         #树干
    "id": 4,
    "name": "dead_tree",
	"type": "good",
    "width": 2,
    "height": 1,
    "gim": "model/dead_tree/dead_tree.gim",
	"good_id": 1001,
}

item_jar = {            #罐子
    "id": 5,
    "name": "jar",
	"type": "none",
    "width": 1,
    "height": 1,
    "gim": "model/jar/jar.gim"
}

item_reed = {           #小草
    "id": 6,
    "name": "reed",
	"type": "unit",
    "width": 0.6,
    "height": 0.6,
    "scale": {
        "x": 1,
        "y": 0.5,
        "z": 1
    },
    "gim": "model/reed/reed.gim",
	"drop_good": 1003,
	"dead #item": "dead_reed",
}

item_dead_reed = {           #小草死亡
    "id": 7,
    "good_id": 1005,
    "name": "dead_reed",
	"type": "none",
    "width": 0.6,
    "height": 0.6,
    "gim": "model/reed/dead_reed.gim"
}

item_stump = {         #树桩
    "id": 8,
    "name": "stump",
	"type": "none",
    "width": 1,
    "height": 1,
    "gim": "model/stump/stump.gim"
}

item_tree = {         #树
    "id": 9,
    "name": "tree",
	"type": "unit",
    "width": 1,
    "height": 1,
	"health": 5,
    "rotation": {
        "x": 0,
        "y @rand.float": (0, 6),
        "z": 0
    },
    "gim": "model/tree/tree.gim",
	"dead #item": "stump",	         #树死亡之后的模型
	"drop_good": 6001,
    "collision": {
        "box": {
            "width": 200, "height": 320, "length": 200
        },
        "center": {
            "x": 0, "y": 160, "z": 0
        }
    }
}

item_withered_tree = {         #树
    "id": 10,
    "name": "withered_tree",
	"type": "unit",
    "width": 1,
    "height": 1,
	"health": 5,
    "gim": "model/withered_tree/withered_tree.gim",
	"dead #item": "stump",	         #树死亡之后的模型
	"drop_good": 6001,
    "collision": {
        "box": {
            "width": 200, "height": 320, "length": 200
        },
        "center": {
            "x": 0, "y": 160, "z": 0
        }
    }
}

data = {
    "berry": item_berry, 1: item_berry,
    "dead_berry": item_dead_berry, 2: item_dead_berry,
    "bush": item_bush, 3: item_bush,
    "dead_tree": item_dead_tree, 4: item_dead_tree,
    "jar": item_jar, 5: item_jar,
    "reed": item_reed, 6: item_reed,
    "dead_reed": item_dead_reed, 7: item_dead_reed,
    "stump": item_stump, 8: item_stump,
    "tree": item_tree, 9: item_tree,
    "withered_tree": item_withered_tree, 10: item_withered_tree
}