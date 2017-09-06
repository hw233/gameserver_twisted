animator_tree = {
    "id": 1,
    "default": "idle",
    "states": {
        "idle": {
            "animation": {
                "name": "idle"
            }
        },

        "hit": {
            "animation": {
                "name": "hit",
            }
        },

        "fall": {
            "animation": {
                "name": "fall",
            }
        }
    },

    "parameters": {
        "hit": {
            "type": "trigger",
            "value": False,
        },
        "fall": {
            "type": "bool",
            "value": False,
        }
    },

    "transitions": {
        "idle": {
            "hit": [
                {
                    "parameter" : "hit",
                    "value": "True",
                }
            ],
            "fall": "fall"
        },
        "hit": {
            "idle": ""
        }
    }
}

data = {
    "tree": animator_tree, 1: animator_tree
}