from math import gcd

import pytest


def parse_input(input_file_path: str):
    output = []
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        text = file.read()
        machines = text.split('\n\n')
        for machine in machines:
            lines = machine.split('\n')
            output.append([split_button_line(lines[0]), split_button_line(lines[1]), split_prize_line(lines[2])])

    return output


def split_button_line(input):
    x_and_y = input.split(':')[1]
    x, y = x_and_y.split(',')
    return int(x.split('+')[1]), int(y.split('+')[1])


def split_prize_line(input):
    x_and_y = input.split(':')[1]
    x, y = x_and_y.split(',')
    return int(x.split('=')[1]), int(y.split('=')[1])


def part1(input_file_path: str):
    inputs = parse_input(input_file_path)
    total_tokens = 0
    prize_count = 0

    for machine in inputs:
        delta_a, delta_b, prize = machine
        result = solve_machine(delta_a, delta_b, prize)

        if result is not None:
            total_tokens += result
            prize_count += 1

    return total_tokens


def solve_machine(delta_a, delta_b, prize):
    dx_a, dy_a = delta_a
    dx_b, dy_b = delta_b
    px, py = prize

    min_tokens = float("inf")

    for a in range(101):
        for b in range(101):
            x_pos = a * dx_a + b * dx_b
            y_pos = a * dy_a + b * dy_b

            if x_pos == px and y_pos == py:
                cost = 3 * a + b
                min_tokens = min(min_tokens, cost)

    return min_tokens if min_tokens != float("inf") else None


def extended_euclidean(a, b):
    if b == 0:
        return (1, 0)
    x, y = extended_euclidean(b, a % b)
    return (y, x - (a // b) * y)


def solve_diophantine(delta_a, delta_b, prize):
    dx_a, dy_a = delta_a
    dx_b, dy_b = delta_b
    px, py = prize

    g = gcd(dx_a, dx_b)
    if px % g != 0:
        return None

    scaled_dx_a, scaled_dx_b, scaled_px = dx_a // g, dx_b // g, px // g
    x, y = extended_euclidean(scaled_dx_a, scaled_dx_b)

    x *= scaled_px
    y *= scaled_px

    results = []
    results.append(solve_machine(x, y, (px,py)))
    return results
    # TODO: A miracle happens

    return None


def part2(input_file_path: str):
    inputs = parse_input(input_file_path)
    total_tokens = 0
    reachable_prizes = 0

    for machine in inputs:
        delta_a, delta_b, prize = machine
        shifted_prize = (prize[0]+ 10 ** 13, prize[1] + 10 ** 13)

        result = solve_diophantine(delta_a, delta_b, shifted_prize)

        if result is not None:
            total_tokens += result
            reachable_prizes += 1

    return total_tokens


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/13/example.txt', 480),
    ('inputs/13/input.txt', 26599)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # ('inputs/13/example.txt', 81),
    # ('inputs/13/input.txt', 1116)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
