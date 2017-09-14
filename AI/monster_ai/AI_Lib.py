from AI import behavior

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
      "child": "2aebd644-4265-4e9d-9127-5cd5645a3c43"
    },
    "2aebd644-4265-4e9d-9127-5cd5645a3c43": {
      "id": "2aebd644-4265-4e9d-9127-5cd5645a3c43",
      "name": "Sequence",
      "title": "Sequence",
      "description": "",
      "properties": {},
      "children": [
        "d4a58acb-8392-4d7e-a452-e2122d8ff246",
        "9125b901-1fae-4401-89df-e38cc106b9f3"
      ]
    },
    "9125b901-1fae-4401-89df-e38cc106b9f3": {
      "id": "9125b901-1fae-4401-89df-e38cc106b9f3",
      "name": "Priority",
      "title": "Priority",
      "description": "",
      "properties": {},
      "children": [
        "0e074647-5176-48f0-8437-f26585a25709",
        "f0e6d8bf-4029-4126-a578-2ce195b07a42",
        "12db7250-7fe8-44d4-810d-48d633781f1e"
      ]
    },
    "0e074647-5176-48f0-8437-f26585a25709": {
      "id": "0e074647-5176-48f0-8437-f26585a25709",
      "name": "Sequence",
      "title": "Sequence",
      "description": "",
      "properties": {},
      "children": [
        "469c71a9-903a-4085-8832-6855561da082",
        "6e9b9a1a-9cba-4690-90d8-c7ffe133333f"
      ]
    },
    "d4a58acb-8392-4d7e-a452-e2122d8ff246": {
      "id": "d4a58acb-8392-4d7e-a452-e2122d8ff246",
      "name": "Beaten",
      "title": "Beaten",
      "description": "",
      "properties": {}
    },
    "469c71a9-903a-4085-8832-6855561da082": {
      "id": "469c71a9-903a-4085-8832-6855561da082",
      "name": "SearchTarget",
      "title": "SearchTarget",
      "description": "",
      "properties": {}
    },
    "6e9b9a1a-9cba-4690-90d8-c7ffe133333f": {
      "id": "6e9b9a1a-9cba-4690-90d8-c7ffe133333f",
      "name": "Route",
      "title": "Route",
      "description": "",
      "properties": {},
    },
    "f0e6d8bf-4029-4126-a578-2ce195b07a42": {
      "id": "f0e6d8bf-4029-4126-a578-2ce195b07a42",
      "name": "Moving",
      "title": "Moving",
      "description": "",
      "properties": {}
    },
    "12db7250-7fe8-44d4-810d-48d633781f1e": {
      "id": "12db7250-7fe8-44d4-810d-48d633781f1e",
      "name": "Idle",
      "title": "Idle",
      "description": "",
      "properties": {},
    }
  },
  "custom_nodes": [
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
    }
  ]
}