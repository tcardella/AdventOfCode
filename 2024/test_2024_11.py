from functools import cache

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return list(map(int, file.read().split()))


def part1(input_file_path: str):
    stones = parse_input(input_file_path)
    return sum(blinker25(stone, 0) for stone in stones)


@cache
def blinker25(stone, blink):
    if blink == 25:
        return 1

    if stone == 0:
        return blinker25(1, blink + 1)

    elif len(str(stone)) % 2 == 0:
        stone_string = str(stone)
        midpoint = int(len(stone_string) / 2)
        return blinker25(int(stone_string[:midpoint]), blink + 1) + blinker25(int(stone_string[midpoint:]), blink + 1)
    else:
        return blinker25(stone * 2024, blink + 1)


@cache
def blinker75(stone, blink):
    if blink == 75:
        return 1

    if stone == 0:
        return blinker75(1, blink + 1)

    elif len(str(stone)) % 2 == 0:
        stone_string = str(stone)
        midpoint = int(len(stone_string) / 2)
        return blinker75(int(stone_string[:midpoint]), blink + 1) + blinker75(int(stone_string[midpoint:]), blink + 1)
    else:
        return blinker75(stone * 2024, blink + 1)


def part2(input_file_path: str):
    stones = parse_input(input_file_path)
    return sum(blinker75(stone, 0) for stone in stones)


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/11/example.txt', 55312),
    ('inputs/11/input.txt', 216996)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/11/input.txt', 257335372288947)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
