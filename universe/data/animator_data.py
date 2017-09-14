animator_tree = {
    "idle": {
        "name": "idle",
        "rate": 1.0
    },
    "hit": {
        "name": "hit",
        "rate": 1.0
    },
    "fall": {
        "name": "fall",
        "rate": 3.0
    },
}

animator_reed = {
    "idle": {
        "name": "idle",
        "rate": 1.0
    },
}

animator_rabbit = {
    "idle": {
        "name": "idle",
        "rate": 1.0
    },
    "run": {
        "name": "run",
        "rate": 1.0
    },
    "die": {
        "name": "die",
        "rate": 1.0
    },
}

animator_monster_01 = {
    "idle": {
        "name": "idle",
        "rate": 1.0
    },
    "hit": {
        "name": "hit",
        "rate": 1.0
    },
    "walk": {
        "name": "walk",
        "rate": 3.0
    },
    "attack": {
        "name": "attack02",
        "rate": 3.0,
        "loop": True
    }
}

data = {
    "tree": animator_tree, 1: animator_tree,
    "reed": animator_reed, 2: animator_reed,
    "rabbit": animator_rabbit, 3: animator_rabbit,
    "monster_01": animator_monster_01, 4: animator_monster_01
}