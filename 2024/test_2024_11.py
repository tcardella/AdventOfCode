from collections import Counter
from functools import cache

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return list(map(int, file.read().split()))
        #return list(file.read().split())


def part1(input_file_path: str):
    stones = parse_input(input_file_path)

    for i in range(25):
        output = []

        for i, stone in enumerate(stones):

            if (stone == 0):
                output.append(1)
            elif len(str(stone)) % 2 == 0:
                stone_string = str(stone)
                midpoint = int(len(stone_string) / 2)

                output.append(int(stone_string[:midpoint]))
                output.append(int(stone_string[midpoint:]))
            else:
                stone *= 2024
                output.append(stone)

        stones = output

    return len(stones)


def part2(input_file_path: str):
    stones = parse_input(input_file_path)


    i = 0
    while i < 75:
        output = []

        for stone in stones:

            if (stone == 0):
                output.append(1)
            elif len(str(stone)) % 2 == 0:
                stone_string = str(stone)
                midpoint = int(len(stone_string) / 2)

                output.append(int(stone_string[:midpoint]))
                output.append(int(stone_string[midpoint:]))
            else:
                stone *= 2024
                output.append(stone)

        stone_counts[i] = len(output)
        stones = output

        i+=1

    print(stone_counts)
    return len(stones)

def part2a(input_file_path: str):
    stones = parse_input(input_file_path)

    count = Counter(len(str(stone)) for stone in stones)

    for _ in range(75):
        new_count = Counter()

        for digit_len, num_stones in count.items():
            if digit_len == 1:
                new_count[1] += num_stones
            elif digit_len % 2 == 0:
                new_len = digit_len // 2
                new_count[new_len] += 2* num_stones
            else:
                prod_len = len(str(2024 * (10 ** (digit_len - 1))))
                new_count[prod_len] += num_stones

        count = new_count

    return sum(count.values())

def part2b(input_file_path: str):
    stones = parse_input(input_file_path)

    state_counts = Counter()

    # Initialize states (group by digit length)
    for stone in stones:
        length = len(str(stone))
        state_counts[length] += 1

    for _ in range(75):
        new_state_counts = Counter()

        for digit_len, count in state_counts.items():
            if digit_len % 2 == 0:
                # Even-digit stones split into two new stones
                new_length = digit_len // 2
                new_state_counts[new_length] += 2 * count
            else:
                # Odd-digit stones grow
                new_length = len(str(2024 * (10 ** (digit_len - 1))))
                new_state_counts[new_length] += count

        # Update the states for the next blink
        state_counts = new_state_counts

    # Compute the total number of stones after all blinks
    total_stones = sum(state_counts.values())
    return total_stones

@cache
def parts(stone, blink):
    if blink == 75:
        return 1

    if stone == 0:
        return parts(1, blink + 1)

    elif len(str(stone)) % 2 == 0:
        stone_string = str(stone)
        midpoint = int(len(stone_string) / 2)
        return parts(int(stone_string[:midpoint]), blink + 1)+ parts(int(stone_string[midpoint:]), blink + 1)
    else:
        return parts(stone * 2024, blink + 1)

def part2c(input_file_path: str):
    stones = parse_input(input_file_path)

    return sum(parts(stone, 0) for stone in stones)

@pytest.mark.parametrize('input_file_path, expected', [
    #('inputs/11/example1.txt', 36),
    ('inputs/11/example2.txt', 55312),
    ('inputs/11/input.txt', 216996)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # ('inputs/11/example1.txt', 81),
    # ('inputs/11/example2.txt', 81),
     ('inputs/11/input.txt', 257335372288947)
])
def test_part_2(input_file_path, expected):
    actual = part2c(input_file_path)
    assert actual == expected
