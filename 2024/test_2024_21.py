import pytest

numeric_keypad = {
    'A': (3, 2),
    '0': (3, 1),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2)
}

directional_keypad = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 0),
    '>': (1, 0),
}


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        codes = []
        for line in file.readlines():
            codes.append(list(line.strip()))
        return codes


def part1(input_file_path: str):
    codes = parse_input(input_file_path)
    return 0


def part2(input_file_path: str):
    towel_patterns, designs = parse_input(input_file_path)
    return 0


coords_to_presses = {
    (1, 0): '^',
    (0, 1): '>',
    (-1, 0): 'v',
    (0, -1): '<'
}


@pytest.mark.parametrize('code, expected', [
    # TODO: Fix these tests
    # ('029A', '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'),
    # ('980A', '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A'),
    # ('179A', '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'),
    # ('456A', '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A'),
    # ('379A', '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A')
])
def test_part_0(code, expected):
    numeric_presses = code_to_numeric_presses(code)
    directional_presses = numeric_presses_to_directional_presses(numeric_presses)
    actual = "".join(directional_presses)
    assert actual == expected

def numeric_presses_to_directional_presses(numeric_presses):
    numeric_presses = ['A'] + numeric_presses
    steps = list(zip(numeric_presses, numeric_presses[1:]))
    presses = []
    for a,b in steps:
        br = directional_keypad[b][0]
        ar = directional_keypad[a][0]
        bc = directional_keypad[b][1]
        ac = directional_keypad[a][1]
        vector = (br - ar, bc - ac)
        if vector[0] > 0:
            char = 'v'
        else:
            char = '^'

        for r in range(abs(vector[0])):
            presses.append(char)

        if vector[1] > 0:
            char = '>'
        else:
            char = '<'

        for c in range(abs(vector[1])):
            presses.append(char)

    return presses

def code_to_numeric_presses(code):
    codes = list(code)
    codes = ['A'] + codes
    steps = list(zip(codes, codes[1:]))
    presses = []
    for a, b in steps:
        br = numeric_keypad[b][0]
        ar = numeric_keypad[a][0]
        bc = numeric_keypad[b][1]
        ac = numeric_keypad[a][1]
        vector = (br - ar, bc - ac)
        if vector[0] > 0:
            char = 'v'
        else:
            char = '^'

        for r in range(abs(vector[0])):
            presses.append(char)

        if vector[1] > 0:
            char = '>'
        else:
            char = '<'

        for c in range(abs(vector[1])):
            presses.append(char)

        presses.append('A')
    return presses


@pytest.mark.parametrize("input_file_path, expected", [
    # TODO: Fix these tests
    # ('inputs/21/example.txt', 126384),
    # ('inputs/21/input.txt', 1351)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # TODO: Fix these tests
    # ('inputs/21/example.txt', 16),
    # ('inputs/21/input.txt', 732978410442050)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
