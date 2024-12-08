import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [line.strip() for line in file.readlines()]


def part1(input_file_path: str):
    map = parse_input(input_file_path)

    start = find_start(map)
    positions = list()
    positions = [pos[0] for pos in find_path(map, positions, start)]
    return len(list(set(positions)))



def find_path(grid, path, start):
    curr_pos = start
    direction = get_next_direction()
    path.append((start, direction))

    while is_in_bounds(curr_pos, grid):
        next_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        if not is_in_bounds(next_pos, grid):
            return path
        if not is_obstruction(next_pos, grid):
            path.append((next_pos, direction))
            curr_pos = next_pos
        else:
            direction = get_next_direction()
    return path

def find_loop(grid, path, start, direction = (0,0)):
    curr_pos = start
    if direction == (0,0):
        direction = get_next_direction()
    path.append((start, direction))

    while is_in_bounds(curr_pos, grid):
        next_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        if not is_in_bounds(next_pos, grid):
            return False
        if not is_obstruction(next_pos, grid):
            if (next_pos, direction) in path:

                print(path)
                return True
            else:
                path.append((next_pos, direction))
                curr_pos = next_pos
        else:
            direction = get_next_direction()
    return False


def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '^':
                return (r, c)
    return (0,0)


def is_obstruction(pos, map):
    return map[pos[0]][pos[1]] == '#'


def is_in_bounds(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
i = 0


def get_next_direction():
    global i
    if i == len(directions):
        i = 0

    dir = directions[i]
    i += 1
    return dir

def turn_right(direction):
    return directions[(directions.index(direction) + 1) % len(directions)]

def part2(input_file_path: str):
    grid = parse_input(input_file_path)
    grid = [list(row) for row in grid]
    count = 0
    start = find_start(grid)
    path = find_path(grid, [], start)
    grid[path[0][0][0]][path[0][0][1]] = '.'

    for i, curr in enumerate(path):
        nx = curr[0][0] + curr[1][0]
        ny = curr[0][1] + curr[1][1]
        next_pos = (nx, ny)

        if is_in_bounds(next_pos, grid):
            if is_obstruction(next_pos, grid):
                continue
            else:
                grid[nx][ny] = '#'
                if find_loop(grid, path[:i], curr[0], curr[1]):
                    print(f"(nx,ny) = ({nx},{ny})")
                    count+=1
                grid[nx][ny] = '.'
        else:
            break

    return count

# @pytest.mark.parametrize('input_file_path, expected', [
#     ('inputs/06/example.txt', 41),
#     ('inputs/06/input.txt', 5318)
# ])
# def test_part_1(input_file_path, expected):
#     actual = part1(input_file_path)
#     assert actual == expected
#
#
# @pytest.mark.parametrize('input_file_path, expected', [
#     ('inputs/06/example.txt', 6),
#     #('inputs/06/input.txt', 5346)
# ])
# def test_part_2(input_file_path, expected):
#     actual = part2(input_file_path)
#     assert actual == expected
