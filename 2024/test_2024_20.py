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


def bfs_shortest_path(maze, start, goal):
    """
    Find the shortest path in a maze using BFS and return the path.

    :param maze: 2D List where 0 represents open path and 1 represents walls.
    :param start: Tuple (x, y) - starting position in the maze.
    :param goal: Tuple (x, y) - goal position in the maze.
    :return: List of tuples representing the path, or an empty list if no path exists.
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited = set()
    visited.add(start)

    # To reconstruct the path, maintain a dictionary of predecessors
    parent_map = {}  # Key: (x, y), Value: predecessor (x, y)

    while queue:
        x, y, distance = queue.popleft()

        # If we reach the goal, reconstruct the path
        if (x, y) == goal:
            return reconstruct_path(parent_map, start, goal)

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and maze[nx][ny] == '.':
                visited.add((nx, ny))
                queue.append((nx, ny, distance + 1))
                parent_map[(nx, ny)] = (x, y)  # Record predecessor for path reconstruction

    # If no path is found, return an empty list
    return []


def reconstruct_path(parent_map, start, goal):
    """
    Reconstruct the path from start to goal using the parent_map.

    :param parent_map: Dictionary mapping each node to its predecessor.
    :param start: Starting position in the maze.
    :param goal: Goal position in the maze.
    :return: List of tuples representing the path from start to goal.
    """
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent_map[current]  # Move to the predecessor
    path.append(start)
    path.reverse()  # Reverse to get the path from start to goal
    return path


def part1(input_file_path: str):
    grid, start, end = parse_input(input_file_path)
    rows = len(grid)
    cols = len(grid[0])

    blank_grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append('.')
        blank_grid.append(row)

    baseline = bfs_shortest_path(grid, start, end)
    baseline_ps = len(baseline) - 1
    count = 0
    cheats = []
    checked = []

    for i, e in enumerate(baseline):
        for f in baseline[i + 1:]:
            count = part1_method2(baseline_ps, blank_grid, cheats, count, e, end, f, grid, start)

        count = part1_method1(grid, baseline_ps, cheats, checked, count, e, end, start)

    return len([e for e in cheats if e >= 100])


def part1_method2(baseline_ps, blank_grid, cheats, count, e, end, f, grid, start):
    if abs(e[0] - f[0]) + abs(e[1] - f[1]) == 2:
        d = bfs_shortest_path(grid, start, e)
        d += bfs_shortest_path(blank_grid, e, f)
        d += bfs_shortest_path(grid, f, end)

        d_ps = len(d) - 1
        if d_ps < baseline_ps:
            cheats.append(baseline_ps - d_ps)
            count += 1
    return count


def part1_method1(grid, baseline_ps, cheats, checked, count, e, end, start):
    rows = len(grid)
    cols = len(grid[0])

    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = e[0] + dr, e[1] + dc

        if (nr, nc) in checked:
            continue
        else:
            checked.append((nr, nc))

        nnr, nnc = nr + dr, nc + dc
        if in_bounds(rows, cols, nr, nc):
            if grid[nr][nc] == '.':
                continue
            if in_bounds(rows, cols, nnr, nnc) and grid[nr][nc] == '#' and grid[nnr][nnc] == '.':
                grid[nr][nc] = '.'
                x = bfs_shortest_path(grid, start, end)
                x_ps = len(x) - 1
                if x_ps < baseline_ps:
                    cheats.append((e, baseline_ps - x_ps))
                    count += 1
                grid[nr][nc] = '#'
    return count


def in_bounds(rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols


def part2(input_file_path: str):
    towel_patterns, designs = parse_input(input_file_path)
    total_arrangements = 0

    return total_arrangements


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/20/example.txt', 0),
    ('inputs/20/input.txt', 1351)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # TODO: Fix these tests
    # ('inputs/20/example.txt', 16),
    # ('inputs/20/input.txt', 732978410442050)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
