
default_tile = {
    0: [{'gim': '00'}],
    1: [{'gim': '10'}, {'gim': '09', 'rotation': {'y': 270}}, {'gim': '05', 'rotation': {'y': 180}}, {'gim': '13', 'rotation': {'y': 90}}],
    2: [{'gim': '09'}, {'gim': '10', 'rotation': {'y': 90}}, {'gim': '05', 'rotation': {'y': 270}}, {'gim': '13', 'rotation': {'y': 180}}],
    3: [{'gim': '01'}, {'gim': '14', 'rotation': {'y': 180}}, {'gim': '08', 'rotation': {'y': 90}}, {'gim': '11', 'rotation': {'y': 270}}],
    4: [{'gim': '13'}, {'gim': '10', 'rotation': {'y': 270}}, {'gim': '09', 'rotation': {'y': 180}}, {'gim': '05', 'rotation': {'y': 90}}],
    5: [{'gim': '08'}, {'gim': '01', 'rotation': {'y': 270}}, {'gim': '14', 'rotation': {'y': 90}}, {'gim': '11', 'rotation': {'y': 180}}],
    6: [{'gim': '06'}, {'gim': '02', 'rotation': {'y': 90}}],
    7: [{'gim': '04'}, {'gim': '12', 'rotation': {'y': 90}}, {'gim': '07', 'rotation': {'y': 270}}, {'gim': '15', 'rotation': {'y': 180}}],
    8: [{'gim': '05'}, {'gim': '10', 'rotation': {'y': 180}}, {'gim': '09', 'rotation': {'y': 90}}, {'gim': '13', 'rotation': {'y': 270}}],
    9: [{'gim': '02'}, {'gim': '06', 'rotation': {'y': 90}}],
    10: [{'gim': '11'}, {'gim': '01', 'rotation': {'y': 90}}, {'gim': '14', 'rotation': {'y': 270}}, {'gim': '08', 'rotation': {'y': 180}}],
    11: [{'gim': '07'}, {'gim': '12', 'rotation': {'y': 180}}, {'gim': '04', 'rotation': {'y': 90}}, {'gim': '15', 'rotation': {'y': 270}}],
    12: [{'gim': '14'}, {'gim': '01', 'rotation': {'y': 180}}, {'gim': '08', 'rotation': {'y': 270}}, {'gim': '11', 'rotation': {'y': 90}}],
    13: [{'gim': '12'}, {'gim': '04', 'rotation': {'y': 270}}, {'gim': '07', 'rotation': {'y': 180}}, {'gim': '15', 'rotation': {'y': 90}}],
    14: [{'gim': '15'}, {'gim': '04', 'rotation': {'y': 180}}, {'gim': '07', 'rotation': {'y': 90}}, {'gim': '12', 'rotation': {'y': 270}}],
    15: [{'gim': '00'}],

    1 + 16 * 2: [{'gim': '16'}],
    2 + 16 * 1: [{'gim': '16', 'scale': {'x': -1.0}}],
    2 + 16 * 8: [{'gim': '16', 'rotation': {'y': 90}}],
    8 + 16 * 2: [{'gim': '16', 'scale': {'x': -1.0}, 'rotation': {'y': 90}}],
    4 + 16 * 8: [{'gim': '16', 'scale': {'z': -1.0}}],
    8 + 16 * 4: [{'gim': '16', 'rotation': {'y': 180}}],
    1 + 16 * 4: [{'gim': '16', 'scale': {'z': -1.0}, 'rotation': {'y': 90}}],
    4 + 16 * 1: [{'gim': '16', 'rotation': {'y': 270}}],

    10 + 16 * 4: [{'gim': '17', 'rotation': {'y': 180}}],
    8 + 16 * 5: [{'gim': '18', 'rotation': {'y': 180}}],
    2 + 16 * 5: [{'gim': '18', 'scale': {'x': -1.0}}],
    10 + 16 * 1: [{'gim': '17', 'scale': {'x': -1.0}}],

    4 + 16 * 3: [{'gim': '18', 'rotation': {'y': 270}}],
    12 + 16 * 1: [{'gim': '17', 'rotation': {'y': 270}}],
    12 + 16 * 2: [{'gim': '17', 'scale': {'x': -1.0}, 'rotation': {'y': 90}}],
    8 + 16 * 3: [{'gim': '18', 'scale': {'x': -1.0}, 'rotation': {'y': 90}}],

    5 + 16 * 8: [{'gim': '17', 'scale': {'z': -1.0}}],
    4 + 16 * 10: [{'gim': '18', 'scale': {'z': -1.0}}],
    5 + 16 * 2: [{'gim': '17'}],
    1 + 16 * 10: [{'gim': '18'}],

    3 + 16 * 8: [{'gim': '17', 'rotation': {'y': 90}}],
    2 + 16 * 12: [{'gim': '18', 'rotation': {'y': 90}}],
    1 + 16 * 12: [{'gim': '18', 'scale': {'z': -1.0}, 'rotation': {'y': 90}}],
    3 + 16 * 4: [{'gim': '17', 'scale': {'z': -1.0}, 'rotation': {'y': 90}}],

    1 + 16 * 8: [{'gim': '19', 'rotation': {'y': 270}}],
    8 + 16 * 1: [{'gim': '19', 'rotation': {'y': 90}}],
    2 + 16 * 4: [{'gim': '19'}],
    4 + 16 * 2: [{'gim': '19', 'rotation': {'y': 180}}],

    6 + 16 * 1: [{'gim': '20', 'rotation': {'y': 270}}],
    9 + 16 * 2: [{'gim': '20'}],
    6 + 16 * 8: [{'gim': '20', 'rotation': {'y': 90}}],
    9 + 16 * 4: [{'gim': '20', 'rotation': {'y': 180}}],

    1 + 16 * 6: [{'gim': '21', 'rotation': {'y': 270}}],
    2 + 16 * 9: [{'gim': '21'}],
    8 + 16 * 6: [{'gim': '21', 'rotation': {'y': 90}}],
    4 + 16 * 9: [{'gim': '21', 'rotation': {'y': 180}}],
}

grass_tile = {
    15: [
        {'gim': '00', 'weight': 300},
        {'gim': '16', 'weight': 5},
        {'gim': '17', 'weight': 5},
        {'gim': '18', 'weight': 5},
        {'gim': '19', 'weight': 5},
        {'gim': '20', 'weight': 5},
        {'gim': '21', 'weight': 1},
        {'gim': '22', 'weight': 1},
        {'gim': '23', 'weight': 1},
        {'gim': '24', 'weight': 5},
        {'gim': '25', 'weight': 5},
        {'gim': '26', 'weight': 5},
        {'gim': '27', 'weight': 5},
        {'gim': '28', 'weight': 1},
        {'gim': '29', 'weight': 2},
        {'gim': '30', 'weight': 1},
        {'gim': '31', 'weight': 2},
    ],
}


data = {
    'default': default_tile,
    'grass': grass_tile,
}
