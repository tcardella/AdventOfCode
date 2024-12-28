from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()
        output = []
        for line in lines:
            parts = line.split(',')
            r, c = int(parts[1]), int(parts[0])
            output.append((r, c))

        return output


def build_grid(rows, cols, coordinates):
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            if (r, c) in coordinates:
                grid[r].append('#')
            else:
                grid[r].append('.')

    return grid


def dump_grid(grid):
    print()
    for row in grid:
        print(''.join(row))
    print()


def part1(input_file_path: str, rows=70, cols=70, b=1024):
    coordinates = parse_input(input_file_path)
    grid = build_grid(rows, cols, coordinates[:b])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    # dump_grid(grid)

    steps = bfs(grid, start, end)
    return len(steps[1:])  # don't count the starting position


def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    queue = deque([start])  # BFS queue
    visited = set()  # Set to track visited nodes
    parent = {}  # Dictionary to store parent nodes for path reconstruction
    visited.add(start)

    # Movement directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()

        # If the goal is reached, reconstruct and return the path
        if current == end:
            path = []
            while current in parent:  # Trace back using parent dictionary
                path.append(current)
                current = parent[current]
            path.append(start)  # Add the start node
            path.reverse()  # Reverse to get the correct order from start to end
            return path

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc

            # Check bounds and if the cell is not already visited
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] == '.':  # Only consider open cells
                    queue.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current  # Track the parent of this node

    return None  # Return None if no path is found


def part2(input_file_path: str, rows=70, cols=70):
    coordinates = parse_input(input_file_path)
    grid = build_grid(rows, cols, [])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    shortest_path = bfs(grid, start, end)

    for r, c in coordinates:
        grid[r][c] = '#'

        if (r, c) in shortest_path:
            shortest_path = bfs(grid, start, end)
            if shortest_path is None:
                return r, c

    return None


@pytest.mark.parametrize("input_file_path, expected, rows, cols, b", [
    ('inputs/18/example.txt', 22, 7, 7, 12),
    ('inputs/18/input.txt', 338, 71, 71, 1024)
])
def test_part_1(input_file_path, expected, rows, cols, b):
    actual = part1(input_file_path, rows, cols, b)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected, rows, cols', [
    ('inputs/18/example.txt', (1, 6), 7, 7),
    ('inputs/18/input.txt', (44,20), 71, 71)
])
def test_part_2(input_file_path, expected, rows, cols):
    actual = part2(input_file_path, rows, cols)
    assert actual == expected
