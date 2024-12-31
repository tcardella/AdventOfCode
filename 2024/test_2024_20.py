from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        grid = [list(line.strip()) for line in file.readlines()]
        start = None
        end = None

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if start and end:
                    break
                elif grid[r][c] == 'S':
                    start = (r, c)
                elif grid[r][c] == 'E':
                    end = (r, c)

    grid[start[0]][start[1]] = '.'
    grid[end[0]][end[1]] = '.'

    return grid, start, end


def part1(input_file_path: str):
    grid, start, end = parse_input(input_file_path)
    rows = len(grid)
    cols = len(grid[0])
    distances = [[-1] * cols for _ in range(rows)]

    r, c = start[0], start[1]
    distances[r][c] = 0

    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:  # down, up, right, left
            # is in bounds and not a wall and has not been visited
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and distances[nr][nc] == -1:
                distances[nr][nc] = distances[r][c] + 1
                queue.append((nr, nc))

    count = 0

    for r in range(rows):
        for c in range(cols):
            # is wall?
            if grid[r][c] == '#':
                continue

            for nr, nc in [(r + 2, c), (r + 1, c + 1), (r, c + 2),
                           (r - 1, c + 1)]:  # down, down and right, right, up and right
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                    continue
                # is wall?
                if grid[nr][nc] == '#':
                    continue
                if abs(distances[r][c] - distances[nr][nc]) >= 102:
                    count += 1

    return count


def part2(input_file_path: str):
    grid, start, end = parse_input(input_file_path)
    rows = len(grid)
    cols = len(grid[0])
    distances = [[-1] * cols for _ in range(rows)]

    r, c = start[0], start[1]
    distances[r][c] = 0

    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:  # down, up, right, left
            # is in bounds and not a wall and has not been visited
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and distances[nr][nc] == -1:
                distances[nr][nc] = distances[r][c] + 1
                queue.append((nr, nc))

    count = 0

    for r in range(rows):
        for c in range(cols):
            # is wall?
            if grid[r][c] == '#':
                continue

            for radius in range(2, 21):
                for dr in range(radius + 1):
                    dc = radius - dr
                    for nr, nc in {(r + dr, c + dc), (r + dr, c - dc), (r - dr, c + dc), (r - dr, c - dc)}:
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                            if (distances[r][c] - distances[nr][nc]) >= 100 + radius:
                                count += 1

    return count


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/20/example.txt', 0),
    ('inputs/20/input.txt', 1351)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/20/example.txt', 0),
    ('inputs/20/input.txt', 966130)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
