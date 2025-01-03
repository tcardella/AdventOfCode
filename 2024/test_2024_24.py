import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        sections = file.read().split('\n\n')
        known_values = {}
        for wire, value in [line.split(':') for line in sections[0].split('\n')]:
            known_values[wire] = int(value)

        formulas = {}
        for line in sections[1].split('\n'):
            a, op, b, _, c = line.split(' ')
            formulas[c] = (a, op, b)

        return known_values, formulas


operators = {
    'OR': lambda a, b: a | b,
    'AND': lambda a, b: a & b,
    'XOR': lambda a, b: a ^ b
}


def part1(input_file_path: str):
    known_values, formulas = parse_input(input_file_path)

    def calc(wire):
        if wire in known_values:
            return known_values[wire]

        a, op, b = formulas[wire]
        known_values[wire] = operators[op](calc(a), calc(b))
        return known_values[wire]

    z = []
    i = 0

    while True:
        key = "z" + str(i).rjust(2, '0')
        if key not in formulas:
            break
        z.append(calc(key))
        i += 1

    output = ''
    for key in reversed(sorted([key for key in known_values.keys() if key.startswith('z')])):
        output += str(known_values[key])
    return int(output, 2)


def part2(input_file_path: str):
    known_values, formulas = parse_input(input_file_path)
    return ''


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/24/example1.txt', 4),
    ('inputs/24/example2.txt', 2024),
    ('inputs/24/input.txt', 45213383376616)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/24/example3.txt', 'aaa,aoc,bbb,ccc,eee,ooo,z24,z99'),
    ('inputs/24/input.txt', 'bw,dr,du,ha,mm,ov,pj,qh,tz,uv,vq,wq,xw')
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
