# coding=utf-8
'''
    :param priority: 优先级，越小的越下面
'''

landform_mud = {
    "id": 1,
    "name": "mud",
    "priority": 0,
    "gim": "scene/mud/mud_%s.gim",
    "transition": {
        2: 5,
        3: 6,
        4: 7
    }
}

landform_grass = {
    "id": 2,
    "name": "grass",
    "priority": 1,
    "gim": "scene/grass/grass_%s.gim",
    "transition": {
        1: 5,
    }
}

landform_withered = {
    "id": 3,
    "name": "withered",
    "priority": 2,
    "gim": "scene/withered/withered_%s.gim",
    "transition": {
        1: 6,
    }
}

landform_marsh = {
    "id": 4,
    "name": "marsh",
    "priority": 3,
    "gim": "scene/marsh/marsh_%s.gim",
    "transition": {
        1: 7,
    }
}

landform_mud_grass = {
    "id": 5,
    "name": "mud_grass",
    "priority": 10,
    "gim": "scene/mud_grass/mud_grass_%s.gim"
}

landform_mud_withered = {
    "id": 6,
    "name": "mud_withered",
    "priority": 10,
    "gim": "scene/mud_withered/mud_withered_%s.gim"
}


landform_mud_marsh = {
    "id": 7,
    "name": "mud_marsh",
    "priority": 10,
    "gim": "scene/mud_marsh/mud_marsh_%s.gim"
}

data = {
    "mud": landform_mud, 1: landform_mud,
    "grass": landform_grass, 2: landform_grass,
    "withered": landform_withered, 3: landform_withered,
    "marsh": landform_marsh, 4: landform_marsh,
    "mud_grass": landform_mud_grass, 5: landform_mud_grass,
    "mud_withered": landform_mud_withered, 6: landform_mud_withered,
    "mud_marsh": landform_mud_marsh, 7: landform_mud_marsh
}