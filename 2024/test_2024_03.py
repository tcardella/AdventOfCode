import re

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return file.readlines()


def part1(input_file_path: str):
    lines = parse_input(input_file_path)
    pattern = r"\b(mul|xmul|do_not_mul)\b\((?P<a>\d+),(?P<b>\d+)\)"
    matches = []
    for line in lines:
        for match in re.finditer(pattern, line):
            matches.append(int(match.group("a")) * int(match.group("b")))

    return sum(matches)


def part2(input_file_path: str):
    lines = parse_input(input_file_path)
    pattern = r"(?P<on>do\(\)|don't\(\))|\b(mul|xmul|do_not_mul)\b\((?P<a>\d+),(?P<b>\d+)\)"
    matches = []
    for line in lines:
        for match in re.finditer(pattern, line):
            if match.group("on"):
                matches.append(match.group("on"))
            elif match.group("a") and match.group("b"):
                matches.append(int(match.group("a")) * int(match.group("b")))

    total = 0
    is_on = True
    for match in matches:
        if match == "don't()":
            is_on = False
        elif match == "do()":
            is_on = True
        else:
            total += int(match) if is_on else 0

    return total


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/03/example1.txt', 161),
    ('inputs/03/input.txt', 175700056)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/03/example2.txt', 48),
    ('inputs/03/input.txt', 71668682)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
