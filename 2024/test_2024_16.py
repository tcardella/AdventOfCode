import heapq

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [list(line.strip()) for line in file.readlines()]


def dfs_maze(maze, start, end, path=None, visited=None):
    """
    Finds all paths from start to end in a given maze using DFS.

    Parameters:
        maze (list of list of int): 2D grid where 0 is an open path, 1 is a wall.
        start (tuple): Starting position as (x, y).
        end (tuple): Ending position as (x, y).
        path (list): The current path being explored (used in recursion).
        visited (set): A set of visited cells to avoid loops (used in recursion).

    Returns:
        list of list of tuple: All paths from start to end.
    """
    if path is None:
        path = []  # Initialize an empty path for the first call
    if visited is None:
        visited = set()  # Initialize the visited set

    x, y = start

    # Add the current cell to the path and mark it as visited
    path.append((x, y))
    visited.add((x, y))

    # If we've reached the end, save the path and return it
    all_paths = []
    if start == end:
        all_paths.append(path[:])  # Copy the current path to avoid mutation
    else:
        # Explore neighbors (up, down, left, right)
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in neighbors:
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and  # Within bounds
                    maze[nx][ny] != '#' and  # Open path
                    (nx, ny) not in visited):  # Not visited yet
                all_paths.extend(dfs_maze(maze, (nx, ny), end, path, visited))

    # Backtrack: remove the current cell from the path and mark it as unvisited
    path.pop()
    visited.remove((x, y))

    return all_paths


def get_neighbors(maze, position):
    """
    Finds all valid neighbors for the given position in the maze.

    Parameters:
        maze (list of list of str): The grid representing the maze.
        position (tuple of int): The current position in the maze as (row, col).

    Returns:
        list of tuple: A list of valid neighboring positions as (row, col).
    """
    neighbors = []
    rows, cols = len(maze), len(maze[0])  # Maze dimensions
    row, col = position

    # Define possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Check all possible neighboring positions
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        # Check if neighbor is within bounds and not a wall ('#')
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            neighbors.append((nr, nc))

    return neighbors


def find_start_and_end(maze):
    start = None
    end = None

    for r in range(len(maze)):
        for c in range(len(maze)):
            if maze[r][c] == 'S':
                start = (r, c)
            if maze[r][c] == 'E':
                end = (r, c)

    return start, end


def part1(input_file_path: str):
    maze = parse_input(input_file_path)
    start, end = find_start_and_end(maze)

    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    pq = []
    heapq.heappush(pq, (0, 0, start, 'right'))

    visited = {}

    while pq:
        score, steps, current, direction = heapq.heappop(pq)

        if current == end:
            return score

        if (current, direction) in visited and visited[(current, direction)] <= score:
            continue
        visited[(current, direction)] = score

        for next_pos in get_neighbors(maze, current):
            next_direction = next_pos[0] - current[0], next_pos[1] - current[1]

            for dir_name, dir_vector in directions.items():
                if next_direction == dir_vector:
                    turn_cost = 0 if dir_name == direction else 1000
                    next_score = score + 1 + turn_cost
                    heapq.heappush(pq, (next_score, steps + 1, next_pos, dir_name))
                    break

    return float('inf')


def dump_grid(maze):
    for r in range(len(maze)):
        print("".join(maze[r]))


def part2(input_file_path: str):
    maze = parse_input(input_file_path)
    start, end = find_start_and_end(maze)

    directions = {(-1, 0),(0, 1),(1, 0),(0, -1)} # up, right, down, left

    pq = []
    visited = set()
    heapq.heappush(pq, (0, start, 3))
    dist = {}
    best_tiles = None

    while pq:
        d, pos, dir = heapq.heappop(pq)
        if (pos, dir) not in dist:
            dist[(pos, dir)] = d
        if pos == end and best_tiles is None:
            best = d
        if (pos, dir) in visited:
            continue
        visited.add((pos, dir))
        dir = directions[dir]
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if 0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] != '#':
            heapq.heappush(pq, (d+1, new_pos, dir))
        heapq.heappush(pq, (d+1000, pos, (dir+1)%4))
        heapq.heappush(pq, (d+1000, pos, (dir+3)%4))

    print(best)

    #     for n in get_neighbors(maze, pos):
    #         for d, v in directions.items():
    #             if n == (pos[0] + v[0], pos[1] + v[1]):
    #                 heapq.heappush(pq, (dist[(pos, dir)] + 1, n, d))
    #
    #     if minimal_score is not None and score > minimal_score:
    #         break
    #
    #     if current == end:
    #         if minimal_score is None:
    #             best_tiles.update(path_tiles)
    #             continue
    #
    #     if (current, direction) in visited and visited[(current, direction)] <= score:
    #         continue
    #     visited[(current, direction)] = score
    #
    #     for next_pos in get_neighbors(maze, current):
    #         next_direction = next_pos[0] - current[0], next_pos[1] - current[1]
    #
    #         for dir_name, dir_vector in directions.items():
    #             if next_direction == dir_vector:
    #                 turn_cost = 0 if dir_name == direction else 1000
    #                 next_score = score + 1 + turn_cost
    #                 next_path_tiles = path_tiles | {next_pos}
    #                 heapq.heappush(pq, (next_score, steps + 1, next_pos, dir_name, next_path_tiles))
    #                 break
    #
    # for p in best_tiles:
    #     maze[p[0]][p[1]] = 'O'
    #
    # dump_grid(maze)

    return len(best_tiles)


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/16/example1.txt', 7036),
    ('inputs/16/example2.txt', 11048),
    ('inputs/16/input.txt', 83444)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # TODO: Fix these tests
    # ('inputs/16/example1.txt', 45),
    # ('inputs/16/example2.txt', 64),
    # ('inputs/16/input.txt', 483)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
