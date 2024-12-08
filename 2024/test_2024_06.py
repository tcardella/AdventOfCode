import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        stripped_lines = [line.strip() for line in file.readlines()]
        return [list(row) for row in stripped_lines]


def part1(input_file_path: str):
    grid = parse_input(input_file_path)

    curr_pos = find_start(grid)
    path = [pos[0] for pos in find_path(grid, curr_pos)]
    return len(list(set(path)))


def find_path(grid, curr_pos):
    direction = directions[0]
    path = [(curr_pos, direction)]

    while is_in_bounds(curr_pos, grid):
        next_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        if not is_in_bounds(next_pos, grid):
            return path
        if not is_obstruction(next_pos, grid):
            path.append((next_pos, direction))
            curr_pos = next_pos
        else:
            direction = turn_right(direction)
    return path


def causes_loop(grid, curr_pos):
    direction = directions[0]
    path = set()

    while is_in_bounds(curr_pos, grid):
        if (curr_pos, direction) in path:
            return True
        path.add((curr_pos, direction))

        next_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        if is_in_bounds(next_pos, grid):
            if not is_obstruction(next_pos, grid):
                curr_pos = next_pos
            else:
                direction = turn_right(direction)
        else:
            return False
    return False


def find_start(grid):
    starts = [(r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == '^']
    return starts[0]


def is_obstruction(pos, grid):
    return grid[pos[0]][pos[1]] == '#'


def is_in_bounds(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def turn_right(direction):
    return directions[(directions.index(direction) + 1) % len(directions)]


def part2(input_file_path: str):
    grid = parse_input(input_file_path)
    count = 0
    curr_pos = find_start(grid)

    empty_positions = set((r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == '.')
    path_positions = set(pos[0] for pos in find_path(grid, curr_pos))
    for r, c in empty_positions.intersection(path_positions):
        grid[r][c] = '#'

        if causes_loop(grid, curr_pos):
            count += 1

        grid[r][c] = '.'

    return count


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/06/example.txt', 41),
    ('inputs/06/input.txt', 5318)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/06/example.txt', 6),
    ('inputs/06/input.txt', 1831)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
