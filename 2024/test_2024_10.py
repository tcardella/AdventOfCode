import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        stripped_lines = [line.strip() for line in file.readlines()]
        grid = [list(row) for row in stripped_lines]

        grid = [[int(value) for value in row] for row in grid]

        return grid


def find_trailheads(grid):
    rows = [row for row in grid]

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                yield row, col


def is_on_map(topographic_map, pos):
    return 0 <= pos[0] < len(topographic_map) and 0 <= pos[1] < len(topographic_map[0])


def move(grid, pos, direction, visited):
    score = 0
    new_pos = pos[0] + direction[0], pos[1] + direction[1]

    if is_on_map(grid, new_pos) and new_pos not in visited :
        if grid[new_pos[0]][new_pos[1]] - grid[pos[0]][pos[1]] == 1:
            print(new_pos)

            visited.add(new_pos)

        if grid[new_pos[0]][new_pos[1]] == 9:
            print("9:", new_pos)
            return 1

        for new_direction in directions:
            score += move(grid, new_pos, new_direction, visited)

        visited.remove(new_pos)

    return score


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def part1(input_file_path: str):
    grid = parse_input(input_file_path)
    trailheads = list(find_trailheads(grid))
    score = 0
    for trailhead in trailheads:
        print()
        print(trailhead)
        visited = set(trailhead)
        for direction in directions:
            score += move(grid, trailhead, direction, visited)

    return score


def part2(input_file_path: str):
    disk_map = parse_input(input_file_path)
    return 0


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/10/example1.txt', 2),
    ('inputs/10/example2.txt', 36),
    # ('inputs/10/input.txt', 6360094256423)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/10/example.txt', 2858),
    ('inputs/10/input.txt', 6379677752410)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
