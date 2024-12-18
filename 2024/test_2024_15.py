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


def is_against_wall(grid, r, c, dr, dc, box_size=1):
    nr, nc = r + dr, c + dc
    if grid[nr][nc] == '#':
        return True
    elif grid[nr][nc] == '.':
        return False
    elif box_size == 1:
        if grid[nr][nc] == 'O':
            return is_against_wall(grid, nr, nc, dr, dc, box_size)
    elif box_size == 2:
        return is_against_wall(grid, nr, nc, dr, dc, box_size)
    else:
        return False


def can_move(grid, r, c, dr, dc, box_size=1):
    nr, nc = r + dr, c + dc

    target = grid[nr][nc]
    if target == '.':
        return True
    if target == '#':
        return False
    # if box_size == 1 and target == 'O':
    if target == 'O':
        if not is_against_wall(grid, nr, nc, dr, dc):
            return True
    # elif box_size == 2 and (target == '[' or target == ']'):
    #     if not is_against_wall(grid, nr, nc, dr, dc) and not is_against_wall(grid, nr + dr, nc + dc, dr, dc):
    #         return True
    if target == '[':
        if dc == 1 or dc == -1:  # from the left or right
            if not is_against_wall(grid, nr, nc, dr, dc) and not is_against_wall(grid, nr + dr, nc + dc, dr, dc):
                return True
        if dr == 1:
            if not is_against_wall(grid, nr, nc, dr, dc) and not is_against_wall(grid, nr, nc + 1, dr, dc):
                return True
        if dr == -1:
            if not is_against_wall(grid, nr, nc, dr, dc) and not is_against_wall(grid, nr, nc + 1, dr, dc):
                return True
    if target == ']':
        if dc == 1 or dc == -1:  # from the left or right
            if not is_against_wall(grid, nr, nc, dr, dc) and not is_against_wall(grid, nr + dr, nc + dc, dr, dc):
                return True
        if dr == 1:
            if not is_against_wall(grid, nr, nc-1, dr, dc) and not is_against_wall(grid, nr, nc, dr, dc):
                return True
        if dr == -1:
            if not is_against_wall(grid, nr, nc-1, dr, dc) and not is_against_wall(grid, nr, nc, dr, dc):
                return True

    return False


def swap(grid, sr, sc, tr, tc, swap_size=1):
    temp = grid[sr][sc]
    grid[sr][sc] = grid[tr][tc]
    grid[tr][tc] = temp


def swap2(grid, s1r, s1c, s2r, s2c, t1r, t1c, t2r, t2c):
    temp1 = grid[s1r][s1c]
    temp2 = grid[s2r][s2c]
    grid[s1r][s1c] = grid[t1r][t1c]
    grid[s2r][s2c] = grid[t2r][t2c]
    grid[t1r][t1c] = temp1
    grid[t2r][t2c] = temp2


def make_move(grid, r, c, dr, dc, box_size=1):
    nr, nc = r + dr, c + dc

    if grid[nr][nc] == '.':
        swap(grid, r, c, nr, nc)
        return nr, nc
    elif box_size == 1:
        if grid[nr][nc] == 'O':
            make_move(grid, nr, nc, dr, dc)
            swap(grid, r, c, nr, nc)
            return nr, nc
        else:
            return r, c
    elif box_size == 2:
        if grid[nr][nc] == '[' or grid[nr][nc] == ']':
            make_move(grid, nr, nc, dr, dc, 2)
            swap(grid, r, c, nr, nc)
            return nr, nc
        else:
            return r, c


def dump_grid(grid):
    for i, row in enumerate(grid):
        print(''.join(row))


def part1(input_file_path: str):
    grid, moves, start = parse_input(input_file_path)

    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    r, c = start

    for move in moves:
        dr, dc = directions[move]
        if can_move(grid, r, c, dr, dc):
            r, c = make_move(grid, r, c, dr, dc)

    gps_sum = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'O':
                gps_sum += 100 * r + c

    return gps_sum


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
    start = find_start(grid)

    directions = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)
    }
    r, c = start

    for move in moves:
        print()
        dump_grid(grid)
        dr, dc = directions[move]
        if can_move(grid, r, c, dr, dc, 2):
            r, c = make_move(grid, r, c, dr, dc, 2)
    print()
    dump_grid(grid)
    gps_sum = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '[':
                gps_sum += 100 * r + c

    return gps_sum


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/15/example0.txt', 2028),
    ('inputs/15/example1.txt', 10092),
    ('inputs/15/input.txt', 1511865)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    # ('inputs/15/example0.txt', 9021),
    # ('inputs/15/example1.txt', 9021),
    ('inputs/15/example2.txt', 9021),

    # ('inputs/15/input.txt', 6576)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
