import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()

    output = []
    for line in lines:
        elements = line.strip().split()
        output.append([int(e) for e in elements])

    return output


def is_safe(levels):
    diffs = [b - a for a, b in zip(levels, levels[1:])]

    increasing = all(0 < diff <= 3 for diff in diffs)
    decreasing = all(-3 <= diff < 0 for diff in diffs)

    return increasing or decreasing


def is_safe_with_dampener(levels):
    if is_safe(levels):
        return True

    for i in range(len(levels)):
        modified_levels = levels[:i] + levels[i + 1:]
        if is_safe(modified_levels):
            return True

    return False


def part1(input_file_path: str):
    reports = parse_input(input_file_path)

    count = 0
    for report in reports:
        if is_safe(report):
            count += 1

    return count


def part2(input_file_path: str):
    reports = parse_input(input_file_path)

    count = 0
    for report in reports:
        if is_safe_with_dampener(report):
            count += 1

    return count


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/02/example.txt', 2),
    ('inputs/02/input.txt', 236)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/02/example.txt', 4),
    ('inputs/02/input.txt', 308)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
