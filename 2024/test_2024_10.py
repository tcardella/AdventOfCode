from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        stripped_lines = [line.strip() for line in file.readlines()]
        grid = [list(row) for row in stripped_lines]

        grid = [[int(value) for value in row] for row in grid]

        return grid


def find_trailheads(grid):
    trailheads = []
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 0:
                trailheads.append((r, c))
    return trailheads


def is_on_map(topographic_map, pos):
    return 0 <= pos[0] < len(topographic_map) and 0 <= pos[1] < len(topographic_map[0])


def bfs(grid, start):
    rows, cols = len(grid), len(grid[0])

    queue = deque([start])
    visited = set()
    reachable_nines = set()

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        current_height = grid[r][c]

        if current_height == 9:
            reachable_nines.add((r, c))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_height = grid[nr][nc]
                if neighbor_height == current_height + 1:
                    queue.append((nr, nc))

    return len(reachable_nines)


def move(grid, pos, direction, visited):
    score = 0
    new_pos = pos[0] + direction[0], pos[1] + direction[1]

    if is_on_map(grid, new_pos) and new_pos not in visited:
        if grid[new_pos[0]][new_pos[1]] - grid[pos[0]][pos[1]] == 1:
            print(new_pos)

            visited.add(new_pos)

        if grid[new_pos[0]][new_pos[1]] == 9:
            print("9:", new_pos)
            score += 1
        else:
            for new_direction in directions:
                score += move(grid, new_pos, new_direction, visited)

        visited.remove(new_pos)

    return score


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def dfs(grid, pos, visited):
    row, col = pos
    current_height = grid[row][col]

    if current_height == 9:
        return 1

    distinct_trails = 0
    visited.add(pos)

    for dr, dc in directions:
        new_pos = row + dr, col + dc
        if is_on_map(grid, new_pos) and new_pos not in visited:
            new_row, new_col = new_pos
            if grid[new_row][new_col] == current_height + 1:
                distinct_trails += dfs(grid, new_pos, visited)

    visited.remove(pos)
    return distinct_trails


def part1(input_file_path: str):
    grid = parse_input(input_file_path)
    trailheads = list(find_trailheads(grid))
    total_score = 0

    for trailhead in trailheads:
        total_score += bfs(grid, trailhead)

    return total_score


def part2(input_file_path: str):
    grid = parse_input(input_file_path)
    trailheads = list(find_trailheads(grid))
    total_rating = 0

    for trailhead in trailheads:
        visited = set()
        total_rating += dfs(grid, trailhead, visited)

    return total_rating


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/10/example.txt', 36),
    ('inputs/10/input.txt', 517)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/10/example.txt', 81),
    ('inputs/10/input.txt', 1116)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
