
ChaseMonster = {
  "id": "d64ad51d-712b-4b47-8e51-c5b4bdc47a7e",
  "title": "Chase AI",
  "description": "",
  "root": "660a8516-6301-4556-9e96-dee66e6fc997",
  "properties": {},
  "nodes": {
    "660a8516-6301-4556-9e96-dee66e6fc997": {
      "id": "660a8516-6301-4556-9e96-dee66e6fc997",
      "name": "Repeater",
      "title": "Repeat <maxLoop>x",
      "description": "",
      "properties": {
        "maxLoop": -1
      },
      "display": {
        "x": -384,
        "y": -144
      },
      "child": "7f9d7cc4-d376-4f97-8010-0cea819848b0"
    },
    "469c71a9-903a-4085-8832-6855561da082": {
      "id": "469c71a9-903a-4085-8832-6855561da082",
      "name": "SearchTarget",
      "title": "SearchTarget",
      "description": "",
      "properties": {},
      "display": {
        "x": 120,
        "y": -168
      }
    },
    "f0e6d8bf-4029-4126-a578-2ce195b07a42": {
      "id": "f0e6d8bf-4029-4126-a578-2ce195b07a42",
      "name": "Moving",
      "title": "Moving",
      "description": "",
      "properties": {},
      "display": {
        "x": 120,
        "y": -84
      }
    },
    "12db7250-7fe8-44d4-810d-48d633781f1e": {
      "id": "12db7250-7fe8-44d4-810d-48d633781f1e",
      "name": "Idle",
      "title": "Idle",
      "description": "",
      "properties": {},
      "display": {
        "x": 120,
        "y": 12
      }
    },
    "aefd1813-015b-448d-81bc-6b7ed1c6a017": {
      "id": "aefd1813-015b-448d-81bc-6b7ed1c6a017",
      "name": "Attack",
      "title": "Attack",
      "description": "",
      "properties": {},
      "display": {
        "x": 120,
        "y": -264
      }
    },
    "7f9d7cc4-d376-4f97-8010-0cea819848b0": {
      "id": "7f9d7cc4-d376-4f97-8010-0cea819848b0",
      "name": "MemSequence",
      "title": "MemSequence",
      "description": "",
      "properties": {},
      "display": {
        "x": -240,
        "y": -144
      },
      "children": [
        "aefd1813-015b-448d-81bc-6b7ed1c6a017",
        "469c71a9-903a-4085-8832-6855561da082",
        "f0e6d8bf-4029-4126-a578-2ce195b07a42",
        "12db7250-7fe8-44d4-810d-48d633781f1e"
      ]
    }
  },
  "display": {
    "camera_x": 960,
    "camera_y": 475,
    "camera_z": 1,
    "x": -576,
    "y": -144
  },
  "custom_nodes": [
    {
      "name": "EnemyFound",
      "category": "condition",
      "title": "enemyfound",
      "description": None,
      "properties": {
        "found_bool": 0
      }
    },
    {
      "name": "Idle",
      "category": "action",
      "title": "Idle",
      "description": None,
      "properties": {}
    },
    {
      "name": "Beaten",
      "category": "action",
      "title": "Beaten",
      "description": None,
      "properties": {}
    },
    {
      "name": "Moving",
      "category": "action",
      "title": "Moving",
      "description": None,
      "properties": {}
    },
    {
      "name": "Route",
      "category": "action",
      "title": "Route",
      "description": None,
      "properties": {}
    },
    {
      "name": "SearchTarget",
      "category": "action",
      "title": "SearchTarget",
      "description": None,
      "properties": {}
    },
    {
      "name": "Attack",
      "category": "action",
      "title": "Attack",
      "description": None,
      "properties": {}
    }
  ]
}