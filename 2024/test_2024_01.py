from collections import Counter

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()

    left, right = [], []
    for line in lines:
        parts = line.strip().split()
        left.append(int(parts[0]))
        right.append(int(parts[-1]))

    return left, right


def part1(input_file_path: str):
    left, right = parse_input(input_file_path)

    left.sort()
    right.sort()

    return sum(abs(l - r) for l, r in zip(left, right))


def part2(input_file_path: str):
    left, right = parse_input(input_file_path)

    right_counter = Counter(right)

    return sum(l * right_counter.get(l, 0) for l in left)


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/01/example.txt', 11),
    ('inputs/01/input.txt', 2086478)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/01/example.txt', 31),
    ('inputs/01/input.txt', 24941624)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
