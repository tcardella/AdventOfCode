import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [line.strip() for line in file.readlines()]


def part1(input_file_path: str):
    map = parse_input(input_file_path)

    positions = [pos[0] for pos in find_path(map)]
    return len(list(set(positions)))



def find_path(map):
    start = find_start(map)
    pace_count = 0
    positions = list()
    curr_pos = start
    direction = get_next_direction()
    positions.append((start, direction))

    while is_in_bounds(curr_pos, map):
        next_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])

        if not is_in_bounds(next_pos, map):
            return positions
        if not is_obstruction(next_pos, map):
            positions.append((next_pos, direction))
            curr_pos = next_pos
            pace_count += 1
        else:
            direction = get_next_direction()
    return positions


def find_start(map):
    rows = len(map)
    cols = len(map[0])
    for r in range(rows):
        for c in range(cols):
            if map[r][c] == '^':
                return (r, c)
    return rows[0], cols[0]


def is_obstruction(pos, map):
    return map[pos[0]][pos[1]] == '#'


def is_in_bounds(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])


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

def find_exclusions(map):
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] == '#' or map[r][c] == '^':
                yield r,c

def part2(input_file_path: str):
    map = parse_input(input_file_path)

    exclusions = list(find_exclusions(map))
    path = find_path(map)
    exclusions.append(path[0][0])

    #for i, (c, n) in enumerate(zip(path, path[1:])):
    turn_count = 0
    direction = path[0][1]
    # for each item in the path, turn right and go until we are no longer in bounds or the position/direction has been visited
    for i, curr in enumerate(path):
        if turn_count < 3:
            if direction != curr[1]:
                direction = curr[1]
                turn_count += 1
                continue
            continue

        next_pos = curr[0] + direction
        #next_pos = (curr[0] + direction[0], curr[1] + direction[1])

        if next_pos in exclusions:
            continue
        else:
            new_obstruction = (next_pos[0], next_pos[1])

        print(path[i-1:i])
        newPath = path[:i]
        direction = turn_right(curr[1])


        # move until we are off the grid (False) or until we hit a visited space (True)

        # count Trues

    # print(((2, 4), (-1, 0)) in path[:3])
    #
    # for y,p in enumerate(path):
    #     print(y,p)



    # x = 0
    # i = 0
    # turn_count = 0
    # direction = path[0][1]
    # # fast forward to the 3rd turn
    # while turn_count < 3:
    #     i += 1
    #     if(direction != path[i][1]):
    #         turn_count += 1
    #
    # print(path[:i])



@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/06/example.txt', 41),
    ('inputs/06/input.txt', 5318)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/06/example.txt', 6),
    #('inputs/06/input.txt', 5346)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
