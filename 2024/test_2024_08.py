import math
from lib2to3.patcomp import tokenize_wrapper

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        stripped_lines = [line.strip() for line in file.readlines()]
        return [list(row) for row in stripped_lines]


def part1(input_file_path: str):
    grid = parse_input(input_file_path)
    antinodes = set()
    antennas = {}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != '.':
                key = grid[r][c]
                if key in antennas.keys():
                    antennas[key].append((r,c))
                else:
                    antennas[key] = [(r,c)]

    for key, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                dx, dy = x2 - x1, y2 - y1
                a1 = (x2 + dx, y2 + dy)
                a2 = (x1 - dx, y1 - dy)

                for ax, ay in (a1, a2):
                    if(0 <= ax < len(grid) and 0 <= ay < len(grid[0])):
                        antinodes.add((ax, ay))

    return len(antinodes)

def part2(input_file_path: str):
    grid = parse_input(input_file_path)

    row_max = len(grid)
    row_min = 0
    col_max = len(grid[0])
    col_min = 0

    antinodes = set()
    antennas = {}
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] != '.':
                key = grid[r][c]
                if key in antennas.keys():
                    antennas[key].append((r, c))
                else:
                    antennas[key] = [(r, c)]

    for key, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                antinodes.add((x1, y1))
                antinodes.add((x2, y2))

                dx, dy = x2 - x1, y2 - y1
                a1 = (x2 + dx, y2 + dy)
                a2 = (x1 - dx, y1 - dy)

                while is_in_grid(grid, a1[0], a1[1]):
                    antinodes.add(a1)
                    a1 = (a1[0] + dx, a1[1] + dy)

                while is_in_grid(grid, a2[0], a2[1]):
                    antinodes.add(a2)
                    a2 = (a2[0] - dx, a2[1] - dy)

    return len(antinodes)


def is_in_grid(grid, ax, ay):
    return 0 <= ax < len(grid) and 0 <= ay < len(grid[0])


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/08/example.txt', 14),
    ('inputs/08/input.txt', 351)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/08/example.txt', 34),
     ('inputs/08/input.txt', 1259)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
