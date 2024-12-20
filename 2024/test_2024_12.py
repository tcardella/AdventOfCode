from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return list(file.read().split())


def is_in_bounds(rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def calculate_area_and_perimeter(grid, rows, cols, row, col, visited):
    queue = deque([(row, col)])
    area = 0
    perimeter = 0
    perimeter_plots = dict()
    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        area += 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if is_in_bounds(rows, cols, nr, nc) and grid[nr][nc] == grid[r][c]:
                queue.append((nr, nc))
            else:
                perimeter += 1
                if (dr, dc) not in perimeter_plots:
                    perimeter_plots[(dr, dc)] = set()
                perimeter_plots[(dr, dc)].add((r, c))
    return area, perimeter, perimeter_plots


def calculate_sides(perimeter_plots):
    side_count = 0
    for k, v in perimeter_plots.items():
        visited = set()
        for (r, c) in v:
            if (r, c) not in visited:
                side_count += 1
                queue = deque([(r, c)])
                while queue:
                    r1, c1 = queue.popleft()
                    if (r1, c1) in visited:
                        continue
                    visited.add((r1, c1))
                    for dr, dc in DIRECTIONS:
                        nr, nc = r1 + dr, c1 + dc
                        if (nr, nc) in v:
                            queue.append((nr, nc))
    return side_count


def get_region_info(grid):
    rows, cols = len(grid), len(grid[0])
    output = []
    visited = set()

    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited:
                continue
            area, perimeter, perimeter_plots = calculate_area_and_perimeter(grid, rows, cols, row, col, visited)
            side_count = calculate_sides(perimeter_plots)
            output.append([(area, perimeter, side_count)])

    return output


def part1(input_file_path: str):
    garden_plot = parse_input(input_file_path)
    region_info = get_region_info(garden_plot)
    total_price = sum(region[0][0] * region[0][1] for region in region_info)
    return total_price


def part2(input_file_path: str):
    garden_plot = parse_input(input_file_path)
    region_info = get_region_info(garden_plot)
    total_price = sum(region[0][0] * region[0][2] for region in region_info)
    return total_price


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/12/example0.txt', 140),
    ('inputs/12/example1.txt', 772),
    ('inputs/12/example.txt', 1930),
    ('inputs/12/input.txt', 1483212)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/12/example0.txt', 80),
    ('inputs/12/example1.txt', 436),
    ('inputs/12/example.txt', 1206),
    ('inputs/12/input.txt', 897062)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
