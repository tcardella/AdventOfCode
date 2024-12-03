import re

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()

    return lines

def part1(input_file_path: str):
    lines = parse_input(input_file_path)

    pattern = r"\b(mul|xmul|do_not_mul)\b\((?P<a>\d+),(?P<b>\d+)\)"

    sum = 0
    for line in lines:
        matches = re.finditer(pattern, line)

        for match in matches:
            sum += (int(match.group("a")) * int(match.group("b")))

    return sum


def part2(input_file_path: str):
    lines = parse_input(input_file_path)

    pattern = r"(?P<on>do\(\)|don't\(\))|\b(mul|xmul|do_not_mul)\b\((?P<a>\d+),(?P<b>\d+)\)"

    output = []
    sum = 0
    for line in lines:
        matches = re.finditer(pattern, line)

        for match in matches:
            if(match.group("on")):
                output.append(match.group("on"))
            elif match.group("a") and match.group("b"):
                output.append(int(match.group("a")) * int(match.group("b")))

    on = True

    for e in range(len(output)):
        if output[e] == "don't()":
            on = False
        elif output[e] == "do()":
            on = True
        else:
            sum += output[e] if on else 0

    return sum


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
