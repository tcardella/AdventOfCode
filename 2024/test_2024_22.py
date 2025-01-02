import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [int(line.strip()) for line in file.readlines()]


def step(num):
    num = (num ^ (num * 64)) % 16777216
    num = (num ^ (num // 32)) % 16777216
    num = (num ^ (num * 2048)) % 16777216
    return num


def part1(input_file_path: str):
    secret_numbers = parse_input(input_file_path)
    total = 0

    for secret_number in secret_numbers:
        for i in range(2000):
            secret_number = step(secret_number)

        total += secret_number

    return total


def part2(input_file_path: str):
    secret_numbers = parse_input(input_file_path)
    changes_to_sum = {}

    for secret_number in secret_numbers:
        buyer = [secret_number % 10]

        for i in range(2000):
            secret_number = step(secret_number)
            buyer.append(secret_number % 10)

        seen = set()
        for i in range(len(buyer) - 4):
            a, b, c, d, e = buyer[i:i + 5]
            temp = (b - a, c - b, d - c, e - d)
            if temp in seen:
                continue
            seen.add(temp)
            if temp not in changes_to_sum:
                changes_to_sum[temp] = 0
            changes_to_sum[temp] += e

    return max(changes_to_sum.values())


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/22/example1.txt', 37327623),
    ('inputs/22/input.txt', 19458130434)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/22/example2.txt', 23),
    ('inputs/22/input.txt', 2130)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
