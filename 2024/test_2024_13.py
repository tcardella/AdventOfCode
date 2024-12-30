import re

import pytest


def parse_input(input_file_path: str):
    output = []
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        for block in file.read().split('\n\n'):
            output.append(map(int, re.findall(r'\d+', block)))
    return output


def part1(input_file_path: str):
    total = 0
    machines = parse_input(input_file_path)
    for machine in machines:
        ax, ay, bx, by, px, py = machine

        # solving for ca and cb in these equations:
        #   ax * ca + bx * cb == px
        #   AND
        #   ay * ca + by * cb == py
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        cb = (px - ax * ca) / bx

        if ca % 1 == cb % 1 == 0:  # is int?
            total += int(ca * 3 + cb)

    return total


def part2(input_file_path: str):
    total = 0
    machines = parse_input(input_file_path)
    for machine in machines:
        ax, ay, bx, by, px, py = machine
        px += 10000000000000
        py += 10000000000000

        # solving for i and j in this equation:
        #   ax * ca + bx * cb == px
        #   AND
        #   ay * ca + by * cb == py
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        cb = (px - ax * ca) / bx

        if ca % 1 == cb % 1 == 0:  # is int?
            total += int(ca * 3 + cb)

    return total


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/13/example.txt', 480),
    ('inputs/13/input.txt', 26599)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/13/input.txt', 106228669504887)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
