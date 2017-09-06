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
            type 类型 fell需要攻击掉落物品, reap收割直接进入背包, good可直接拾取, none不可交互
            reaped 采集后变为
            good 物品ID
            reap_time 采集时间
'''

BERRY_ID = 1
REAPED_BERRY_ID = 2
BERRY_FRUIT_ID = 3
REED_ID = 4
REAPED_REED_ID = 5
REED_LEAF_ID = 6
TREE_ID = 7
WITHERED_TREE_ID = 8
STUMP_ID = 9
WOOD_ID = 10
BRANCH_ID = 11

JAR_ID = 101
STONE01_ID = 102
STONE02_ID = 103
STONE03_ID = 104
STONE04_ID = 105
BOX01_ID = 110
CASK_ID = 121
BUSH_ID = 122
WEEDS_ID = 123

AXE_ID = 2001
HAMMER_ID = 2002
LANCE_ID = 2003
DAGGER_ID = 2004

WOOD_SHIELD_ID = 3001
IRON_SHIELD_ID = 3002

HAT_ID = 4001
ADVANCED_HAT_ID = 4002

EGG_ID = 6002
MEAT_ID = 6003


item_berry = {
    # 整株浆果
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/berry/berry.gim",
        },
        {
            "comp": "item",
            "id": BERRY_ID,
            "name": "berry",
            "kind": "reap",
            "health": 50,
            "reaped": "reaped_berry",
            "good": 6001,
            "reap_time": 1,
        }
    ],
}

item_reaped_berry = {
    # 收割后的浆果
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/berry/reaped_berry.gim",
        },
        {
            "comp": "item",
            "id": REAPED_BERRY_ID,
            "name": "reaped_berry",
            "kind": "none",
        }
    ],
}

item_berry_fruit = {
    # 浆果果实
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/berry/berry_obj.gim",
        },
        {
            "comp": "item",
            "id": BERRY_FRUIT_ID,
            "name": "berry_fruit",
            "kind": "good",
            "good": 6001
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
            "comp": "renderer",
            "gim": "model/reed/reed.gim",
        },
        {
            "comp": "item",
            "id": REED_ID,
            "name": "reed",
            "kind": "reap",
            "health": 10,
            "good": 1003,
            "reaped": "reaped_reed",
        }
    ],
}

item_reaped_reed= {
    # 采集过后的草
    "creator": {
        "range": 50
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/reed/reaped_reed.gim",
        },
        {
            "comp": "item",
            "id": REAPED_REED_ID,
            "name": "reaped_reed",
            "kind": "none"
        }
    ],
}

item_reed_leaf = {
    # 小草的叶子
    "creator": {
        "range": 50
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/reed/reed_obj.gim",
        },
        {
            "comp": "item",
            "id": REED_LEAF_ID,
            "name": "reed_leaf",
            "kind": "good",
            "good": 1003,
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
            "id": TREE_ID,
            "name": "tree",
            "kind": "fell",
            "health": 50,
            "reaped": "stump",
            "good": "wood",
        }
    ],
}

item_withered_tree = {
    # 枯树
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
            "id": WITHERED_TREE_ID,
            "name": "withered_tree",
            "kind": "fell",
            "health": 100,
            "reaped": "stump",
            "good": "wood",
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
            "comp": "renderer",
            "gim": "model/stump/stump.gim",
        },
        {
            "comp": "item",
            "id": STUMP_ID,
            "name": "stump",
            "kind": "none",
        }
    ],
}

item_wood = {
    # 木头
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/wood/wood.gim",
        },
        {
            "comp": "item",
            "id": WOOD_ID,
            "name": "wood",
            "kind": "good",
            "good": 1002,
        }
    ],
}

item_branch = {
    # 树干
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/branch/branch.gim",
        },
        {
            "comp": "item",
            "id": BRANCH_ID,
            "name": "branch",
            "kind": "good",
            "good": 1001,
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
            "comp": "renderer",
            "gim": "model/jar/jar.gim",
        },
        {
            "comp": "item",
            "id": JAR_ID,
            "name": "jar",
            "kind": "none",
        }
    ],
}


item_stone01 = {
    # 石头
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/stone/stone_01.gim",
        },
        {
            "comp": "item",
            "id": STONE01_ID,
            "name": "stone01",
            "kind": "none",
        }
    ],
}

item_stone02 = {
    # 石头
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/stone/stone_02.gim",
        },
        {
            "comp": "item",
            "id": STONE02_ID,
            "name": "stone02",
            "kind": "none",
        }
    ],
}

item_stone03 = {
    # 石头
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/stone/stone_03.gim",
        },
        {
            "comp": "item",
            "id": STONE03_ID,
            "name": "stone03",
            "kind": "none",
        }
    ],
}

item_stone04 = {
    # 石头
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/stone/stone_04.gim",
        },
        {
            "comp": "item",
            "id": STONE04_ID,
            "name": "stone04",
            "kind": "none",
        }
    ],
}


item_box01 = {
    # 盒子
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/box/box_01.gim",
        },
        {
            "comp": "item",
            "id": BOX01_ID,
            "name": "box01",
            "kind": "none",
        }
    ],
}

item_cask = {
    # 木头
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/cask/cask.gim",
        },
        {
            "comp": "item",
            "id": CASK_ID,
            "name": "cask",
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
            "comp": "renderer",
            "gim": "model/bush/bush.gim",
        },
        {
            "comp": "item",
            "id": BUSH_ID,
            "name": "bush",
            "kind": "none",
        }
    ],
}

item_weeds = {
    # 装饰性小草片
    "creator": {
        "range": 80
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/weeds/weeds_grass.gim",
        },
        {
            "comp": "item",
            "id": WEEDS_ID,
            "name": "weeds",
            "kind": "none",
        }
    ],
}

item_axe = {
    # 斧头
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "player/explorer/axe.gim",
        },
        {
            "comp": "item",
            "id": AXE_ID,
            "name": "axe",
            "kind": "good",
            "good": 2001,
        }
    ],
}

item_hammer = {
    # 锤子
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/hammer/hammer.gim",
        },
        {
            "comp": "item",
            "id": HAMMER_ID,
            "name": "hammer",
            "kind": "good",
            "good": 2001,
        }
    ],
}

item_lance = {
    # 标枪
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "player/explorer/lance.gim",
        },
        {
            "comp": "item",
            "id": LANCE_ID,
            "name": "lance",
            "kind": "good",
            "good": 2003,
        }
    ],
}

item_dagger = {
    # 匕首
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "player/explorer/dagger.gim",
        },
        {
            "comp": "item",
            "id": DAGGER_ID,
            "name": "dagger",
            "kind": "good",
            "good": 2004,
        }
    ],
}

item_wood_shield = {
    # 木盾牌
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "player/explorer/shield.gim",
        },
        {
            "comp": "item",
            "id": WOOD_SHIELD_ID,
            "name": "wood_shield",
            "kind": "good",
            "good": 3001,
        }
    ],
}

item_iron_shield = {
    # 铁盾牌
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "player/explorer/shield.gim",
        },
        {
            "comp": "item",
            "id": IRON_SHIELD_ID,
            "name": "iron_shield",
            "kind": "good",
            "good": 3002,
        }
    ],
}

item_hat = {
    # 帽子
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/hat/hat.gim",
        },
        {
            "comp": "item",
            "id": HAT_ID,
            "name": "hat",
            "kind": "good",
            "good": 4001,
        }
    ],
}

item_advanced_hat = {
    # 加强的帽子
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/hat/hat.gim",
        },
        {
            "comp": "item",
            "id": ADVANCED_HAT_ID,
            "name": "hat",
            "kind": "good",
            "good": 4002,
        }
    ],
}

item_egg = {
    # 鸟蛋
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/egg/egg.gim",
        },
        {
            "comp": "item",
            "id": EGG_ID,
            "name": "egg",
            "kind": "good",
            "good": 6002,
        }
    ],
}

item_meat = {
    # 大肉
    "creator": {
        "range": 100
    },
    "components": [
        {
            "comp": "renderer",
            "gim": "model/meat/meat.gim",
        },
        {
            "comp": "item",
            "id": MEAT_ID,
            "name": "meat",
            "kind": "good",
            "good": 6003,
        }
    ],
}

data = {
    "berry": item_berry, BERRY_ID: item_berry,
    "reaped_berry": item_reaped_berry, REAPED_BERRY_ID: item_reaped_berry,
    "berry_fruit": item_berry_fruit, BERRY_FRUIT_ID: item_berry_fruit,

    "reed": item_reed, REED_ID: item_reed,
    "reaped_reed": item_reaped_reed, REAPED_REED_ID: item_reaped_reed,
    "reed_leaf": item_reed_leaf, REED_LEAF_ID: item_reed_leaf,

    "tree": item_tree, TREE_ID: item_tree,
    "withered_tree": item_withered_tree, WITHERED_TREE_ID: item_withered_tree,
    "stump": item_stump, STUMP_ID: item_stump,
    "wood": item_wood, WOOD_ID: item_wood,
    "branch": item_branch, BRANCH_ID: item_branch,

    "jar": item_jar, JAR_ID: item_jar,
    "stone01": item_stone01, STONE01_ID: item_stone01,
    "stone02": item_stone02, STONE02_ID: item_stone02,
    "stone03": item_stone03, STONE03_ID: item_stone03,
    "stone04": item_stone04, STONE04_ID: item_stone04,
    "box01": item_box01, BOX01_ID: item_box01,
    "cask": item_cask, CASK_ID: item_cask,
    "bush": item_bush, BUSH_ID: item_bush,
    "weeds": item_weeds, WEEDS_ID: item_weeds,

    "axe": item_axe, AXE_ID: item_axe,
    "hammer": item_hammer, HAMMER_ID: item_hammer,
    "lance": item_lance, LANCE_ID: item_lance,
    "dagger": item_dagger, DAGGER_ID: item_dagger,

    "wood_shield": item_wood_shield, WOOD_SHIELD_ID: item_wood_shield,
    "iron_shield": item_iron_shield, IRON_SHIELD_ID: item_iron_shield,

    "hat": item_hat, HAT_ID: item_hat,
    "advanced": item_advanced_hat, ADVANCED_HAT_ID: item_advanced_hat,

    "egg": item_egg, EGG_ID: item_egg,
    "meat": item_meat, MEAT_ID: item_meat,
}