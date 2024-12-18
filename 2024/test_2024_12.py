from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return list(file.read().split())


def find_regions(garden_plot):
    rows, cols = len(garden_plot), len(garden_plot[0])
    regions = {}

    for r in range(rows):
        for c in range(cols):
            if garden_plot[r][c] not in regions:
                regions[garden_plot[r][c]] = (r, c)

    return regions


def find_region(garden_plot, region):
    rows, cols = len(garden_plot), len(garden_plot[0])
    for r in range(rows):
        for c in range(cols):
            if garden_plot[r][c] == region:
                return r, c


def part1(input_file_path: str):
    garden_plot = parse_input(input_file_path)

    total_price = 0
    x = get_areas_and_perimeters(garden_plot)
    for e in x:
        total_price += e[0][0] * e[0][1]

    return total_price


def is_in_bounds(rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols


def get_areas_and_perimeters(grid):
    rows, cols = len(grid), len(grid[0])
    output = []
    visited = set()

    region = ''
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited and grid[row][col] != region:
                region = grid[row][col]
                visited.add((row, col))
                queue = deque([(row, col)])
                perimeter = 0
                area = 0

                while queue:
                    r, c = queue.popleft()
                    area += 1
                    local_perimeter = 4

                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] == region:
                                local_perimeter -= 1

                                if (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))

                    perimeter += local_perimeter

                output.append([(area, perimeter)])
                region = ''

    return output


def get_areas_and_sides(garden_plot, region, row, col, visited):
    rows, cols = len(garden_plot), len(garden_plot[0])
    queue = deque([(row, col)])
    visited.add((row, col))
    area = 0
    sides = 0

    while queue:
        r, c = queue.popleft()
        area += 1

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if not is_in_bounds(rows, cols, nr, nc) or garden_plot[nr][nc] != region:
                print(nr, nc)
                sides += 1
            elif (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return area, sides


def dfs(garden_plot, r, c, visited, region):
    rows, cols = len(garden_plot), len(garden_plot[0])
    stack = [(r,c)]
    visited.add((r, c))
    area = 0
    sides = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        cr, cc = stack.pop()
        area += 1

        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc

            if not is_in_bounds(rows, cols, nr, nc) or garden_plot[nr][nc] != region:
                sides += 1
            else:
                if (nr,nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr,nc))

    return area, sides


def part2(input_file_path: str):
    garden_plot = parse_input(input_file_path)
    regions = find_regions(garden_plot)
    total_price = 0

    for key, region in regions.items():
        for i, (perimeter, area, sides) in enumerate(region, 1):
            total_price += area * sides

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
    ('inputs/12/input.txt', 1483212)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
