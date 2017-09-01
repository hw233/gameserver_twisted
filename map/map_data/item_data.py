# coding=utf-8

'''
结构说明:
    id 种类id
    components 组件集合
        - transform
            position
            rotation
            scale

        - renderer
            gim 模型

        - item
            type 类型 unit需要攻击, good可直接拾取, none不可交互
            reaped 采集后对应的物品
            drop_good 物件死亡之后，掉落的物品
            good_id 当类型为goods时，填写为物品ID
'''

item_berry = {
    # 浆果
    "creator": {
        "range": 100
    },
    "components":[
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 60,
                "height": 50,
                "length": 70,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/berry/berry.gim",
        },
        {
            "comp": "item",
            "id": 1,
            "name": "berry",
            "kind": "unit",
            "health": 50,
            "reaped #item": "berry_reaped",
            "drop_good": 6001,
            "collect_time": 1,
        }
    ],
}

item_berry_reaped = {
    # 收割后的浆果
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/berry/dead_berry.gim",
        },
        {
            "comp": "item",
            "id": 2,
            "name": "berry_reaped",
            "kind": "none",
        }
    ],
}

item_bush = {
    # 草丛
    "creator": {
        "range": 250
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 250,
                "height": 100,
                "length": 230,
            },
            "center": {
                "x": 0, "y": 50, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/bush/bush.gim",
        },
        {
            "comp": "item",
            "id": 3,
            "name": "bush",
            "kind": "none",
        }
    ],
}

item_tree_reaped = {
    # 树干
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/dead_tree/dead_tree.gim",
        },
        {
            "comp": "item",
            "id": 4,
            "name": "tree_reaped",
            "kind": "good",
            "good_id": 1001,
        }
    ],
}

item_jar = {
    # 罐子

    "creator": {
        "range": 50
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/jar/jar.gim",
        },
        {
            "comp": "item",
            "id": 5,
            "name": "jar",
            "kind": "none",
        }
    ],
}

item_reed = {
    # 小草

    "creator": {
        "range": 50
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/reed/reed.gim",
        },
        {
            "comp": "item",
            "id": 6,
            "name": "reed",
            "kind": "unit",
            "drop_good": 1003,
            "reaped #item": "reed_reaped",
        }
    ],
}

item_reed_reaped = {
    # 死草
    "creator": {
        "range": 50
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/reed/dead_reed.gim",
        },
        {
            "comp": "item",
            "id": 7,
            "name": "reed_reaped",
            "kind": "none",
            "drop_good": 1005,
        }
    ],
}

item_stump = {
    # 树桩
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 50,
                "height": 50,
                "length": 50,
            },
            "center": {
                "x": 0, "y": 25, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/stump/stump.gim",
        },
        {
            "comp": "item",
            "id": 8,
            "name": "stump",
            "kind": "none",
            "drop_good": 1005,
        }
    ],
}

item_tree = {
    # 树
    "creator": {
        "range": 150
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 150,
                "height": 500,
                "length": 150,
            },
            "center": {
                "x": 0, "y": 250, "z": 0
            },
            "outline_visible": False
        },
        {
            "comp": "renderer",
            "gim": "model/tree/tree.gim",
        },
        {
            "comp": "item",
            "id": 9,
            "name": "tree",
            "kind": "unit",
            "health": 50,
            "reaped #item": "stump",
            "drop_good": 6001,
        }
    ],
}

item_withered_tree = {
    # 枯树
    "id": 10,
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "collider",
            "type": "AABB",
            "shape": {
                "width": 80,
                "height": 300,
                "length": 80,
            },
            "center": {
                "x": 0, "y": 150, "z": -10
            },
            "outline_visible": False
        },
        {
            "comp": "animator",
            "#animator": "tree"
        },
        {
            "comp": "renderer",
            "gim": "model/withered_tree/withered_tree.gim",
        },
        {
            "comp": "item",
            "name": "withered_tree",
            "kind": "unit",
            "reaped #item": "stump",
            "drop_good": 6001,
        }
    ],
}

data = {
    "berry": item_berry, 1: item_berry,
    "berry_reaped": item_berry_reaped, 2: item_berry_reaped,
    "bush": item_bush, 3: item_bush,
    "tree_reaped": item_tree_reaped, 4: item_tree_reaped,
    "jar": item_jar, 5: item_jar,
    "reed": item_reed, 6: item_reed,
    "reed_reaped": item_reed_reaped, 7: item_reed_reaped,
    "stump": item_stump, 8: item_stump,
    "tree": item_tree, 9: item_tree,
    "withered_tree": item_withered_tree, 10: item_withered_tree
}