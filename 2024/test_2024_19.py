import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        text = file.read()
        sections = text.split('\n\n')
        towel_patterns = [e.strip() for e in sections[0].split(',')]
        designs = [e.strip() for e in sections[1].split('\n')]

        return towel_patterns, designs


def is_possible_to_form(design, towel_patterns):
    def can_form(target):
        if target in memo:
            return memo[target]
        if not target:
            return True
        for pattern in towel_patterns:
            if target.startswith(pattern):
                if can_form(target[len(pattern):]):
                    memo[target] = True
                    return True
        memo[target] = False
        return False

    memo = {}
    return can_form(design)


def count_ways(design, towel_patterns):
    def num_ways(target):
        if target in memo:
            return memo[target]
        if not target:
            return 1

        total = 0
        for pattern in towel_patterns:
            if target.startswith(pattern):
                total += num_ways(target[len(pattern):])
        memo[target] = total
        return total

    memo = {}
    return num_ways(design)


def part1(input_file_path: str):
    towel_patterns, designs = parse_input(input_file_path)

    count = 0

    for design in designs:
        if is_possible_to_form(design, towel_patterns):
            count += 1

    return count


def part2(input_file_path: str):
    towel_patterns, designs = parse_input(input_file_path)
    total_arrangements = 0

    for design in designs:
        total_arrangements += count_ways(design, towel_patterns)

    return total_arrangements


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/19/example.txt', 6),
    ('inputs/19/input.txt', 355)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/19/example.txt', 16),
    ('inputs/19/input.txt', 732978410442050)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
