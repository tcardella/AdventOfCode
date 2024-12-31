import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        text = file.read()
        grid_and_moves = text.split('\n\n')
        grid = [list(row) for row in grid_and_moves[0].split('\n')]
        moves = "".join(grid_and_moves[1].split('\n'))
        start = find_start(grid)

        return grid, moves, start


def find_start(grid):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                return r, c


def part1(input_file_path: str):
    grid, moves, start = parse_input(input_file_path)
    rows, cols = len(grid), len(grid[0])

    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    r, c = start

    for move in moves:
        dr, dc = directions[move]
        targets = [(r, c)]
        cr = r
        cc = c
        can_move = True
        while True:
            cr += dr
            cc += dc
            e = grid[cr][cc]
            if e == '#':
                can_move = False
                break
            elif e == 'O':
                targets.append((cr, cc))
            elif e == '.':
                break

        if not can_move:
            continue

        grid[r][c] = '.'  # move the robot from its original spot
        grid[r + dr][c + dc] = '@'  # move the robot to its new spot
        for br, bc in targets[1:]:  # first element is the robot
            grid[br + dr][bc + dc] = 'O'

        r += dr
        c += dc

    return sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == 'O')


def expand_grid(grid):
    new_grid = []
    for r in range(len(grid)):
        row = ''
        for c in range(len(grid[r])):
            if grid[r][c] == '#':
                row += '##'
            elif grid[r][c] == 'O':
                row += '[]'
            elif grid[r][c] == '.':
                row += '..'
            elif grid[r][c] == '@':
                row += '@.'
        new_grid.append(list(row))
    return new_grid


def part2(input_file_path: str):
    grid, moves, start = parse_input(input_file_path)
    grid = expand_grid(grid)
    rows, cols = len(grid), len(grid[0])
    start = find_start(grid)

    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    r, c = start

    for move in moves:
        dr, dc = directions[move]
        targets = [(r, c)]
        can_move = True
        for cr, cc in targets:
            nr = cr + dr
            nc = cc + dc
            if (nr, nc) in targets:
                continue
            e = grid[nr][nc]
            if e == '#':
                can_move = False
                break
            elif e == '[':  # if one of the halves is found, add the other half
                targets.append((nr, nc))
                targets.append((nr, nc + 1))
            elif e == ']':  # if one of the halves is found, add the other half
                targets.append((nr, nc))
                targets.append((nr, nc - 1))
        if not can_move:
            continue

        copy = [list(row) for row in grid]  # deepcopy
        grid[r][c] = '.'  # move the robot from its original spot
        grid[r + dr][c + dc] = '@'  # move the robot to its new spot
        for br, bc in targets[1:]:  # first element is the robot
            grid[br][bc] = '.'
        for br, bc in targets[1:]:  # first element is the robot
            grid[br + dr][bc + dc] = copy[br][bc]

        r += dr
        c += dc

    return sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == '[')


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/15/example0.txt', 2028),
    ('inputs/15/example1.txt', 10092),
    ('inputs/15/input.txt', 1511865)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/15/example0.txt', 1751),
    ('inputs/15/example1.txt', 9021),
    ('inputs/15/example2.txt', 618),
    ('inputs/15/input.txt', 1519991)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
