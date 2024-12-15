import pytest

DURATION_IN_SECONDS = 100


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()

        pos_and_vectors = [line.split(' ') for line in lines]
        output = []

        for pos_and_vector in pos_and_vectors:
            pos = pos_and_vector[0].split('=')
            vector = pos_and_vector[1].split('=')
            p0 = pos[1].split(',')
            p1 = (int(p0[0]), int(p0[1]))
            v0 = vector[1].split(',')
            v1 = (int(v0[0]), int(v0[1].strip()))
            output.append([p1, v1])

    return output


def part1(input_file_path: str, width=101, height=103):
    pos_and_vector = parse_input(input_file_path)
    positions = []
    for pos, vector in pos_and_vector:
        new_pos = (pos[0] + vector[0] * DURATION_IN_SECONDS, pos[1] + vector[1] * DURATION_IN_SECONDS)
        new_pos = (new_pos[0] % width, new_pos[1] % height)
        positions.append(new_pos)

    qWidth = width // 2
    qHeight = height // 2
    quadrants = [
        [(0, 0), (qWidth, qHeight)],
        [(width - qWidth, 0), (width, qHeight)],
        [(0, height - qHeight), (qWidth, height)],
        [(width - qWidth, height - qHeight), (width, height)]
    ]
    factors = {1: 0, 2: 0, 3: 0, 4: 0}

    for i, q in enumerate(quadrants):
        for p in positions:
            if q[0][0] <= p[0] < q[1][0] and q[0][1] <= p[1] < q[1][1]:
                factors[i + 1] += 1

    safety_factor = 1
    for k, v in factors.items():
        safety_factor *= v
    return safety_factor


def part2(input_file_path: str):
    pos_and_vectors = parse_input(input_file_path)
    smallest_group_count = float('inf')
    best_time = 0
    best_positions = []

    for i in range(6580):
        for e in pos_and_vectors:
            nx = (e[0][0] + e[1][0]) % 101
            ny = (e[0][1] + e[1][1]) % 103
            e[0] = (nx, ny)

        group_count = len(group_points([(p[0][0], p[0][1]) for p in pos_and_vectors]))
        if group_count < smallest_group_count:
            smallest_group_count = group_count
            best_time = i
            best_positions = [(p[0][0], p[0][1]) for p in pos_and_vectors]

    print_grid(best_positions, best_time)

    return best_time


def group_points(points):
    points_set = set(points)
    visited = set()
    groups = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(point, group):
        stack = [point]
        while stack:
            curr = stack.pop()
            if curr in visited:
                continue
            visited.add(curr)
            group.append(curr)

            for dx, dy in directions:
                neighbor = (curr[0] + dx, curr[1] + dy)
                if neighbor in points_set and neighbor not in visited:
                    stack.append(neighbor)

    for point in points:
        if point not in visited:
            group = []
            dfs(point, group)
            groups.append(group)

    return groups


def print_grid(best_positions, i):
    print()
    print(i)
    grid = [['.' for _ in range(101)] for _ in range(103)]
    for x, y in best_positions:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))


@pytest.mark.parametrize('input_file_path, expected, width, height', [
    ('inputs/14/example.txt', 12, 11, 7),
    ('inputs/14/input.txt', 229421808, 101, 103)
])
def test_part_1(input_file_path, expected, width, height):
    actual = part1(input_file_path, width, height)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/14/input.txt', 6576)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
