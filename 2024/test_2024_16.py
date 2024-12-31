import heapq
from collections import deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        maze = [list(line.strip()) for line in file.readlines()]
    start = None
    end = None
    for r in range(len(maze)):
        for c in range(len(maze)):
            if maze[r][c] == 'S':
                start = (r, c)
            if maze[r][c] == 'E':
                end = (r, c)
    return maze, start, end


def part1(input_file_path: str):
    maze, start, end = parse_input(input_file_path)

    # cost, start R, start C, direction R, direction C
    pq = [(0, start[0], start[1], 0, 1)]
    visited = {(start[0], start[1], 0, 1)}

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)  # get next cheapest option
        visited.add((r, c, dr, dc))

        # is this the end?
        if (r, c) == end:
            return cost

        possible_moves = [
            (cost + 1, r + dr, c + dc, dr, dc),  # move forward from r,c in the current direction
            (cost + 1000, r, c, dc, -dr),  # turn clockwise and move forward from r,c
            (cost + 1000, r, c, -dc, dr)  # turn counter-clockwise and move forward from r,c
        ]

        for new_cost, nr, nc, ndr, ndc in possible_moves:
            # can't move into a wall
            if maze[nr][nc] == '#':
                continue

            # have we visited nr,nc facing ndr,ndc?
            if (nr, nc, ndr, ndc) in visited:
                continue

            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))


def part2(input_file_path: str):
    maze, start, end = parse_input(input_file_path)

    # cost, start R, start C, direction R, direction C
    pq = [(0, start[0], start[1], 0, 1)]
    lowest_cost = {(start[0], start[1], 0, 1): 0}  # for each state (pos + dir), what is the lowest cost to get there?
    backtrack = {}  # all the states that could get to the end
    best_cost = float('inf')  # holds the lowest cost to get to the end
    end_states = set()  # list of all possible states to get to the end

    # tldr; Dijkstra's algorithm to find all paths to the end
    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)  # get next cheapest option

        # if state is worse (greater than) the lowest, skip it
        if cost > lowest_cost.get((r, c, dr, dc), float("inf")):
            continue

        # is this the end?
        if (r, c) == end:
            # if we've processed all the best ways to get to the end
            if cost > best_cost:
                break
            best_cost = cost
            end_states = {(r, c, dr, dc)}

        possible_moves = [
            (cost + 1, r + dr, c + dc, dr, dc),  # move forward from r,c in the current direction
            (cost + 1000, r, c, dc, -dr),  # turn clockwise and move forward from r,c
            (cost + 1000, r, c, -dc, dr)  # turn counter-clockwise and move forward from r,c
        ]

        for new_cost, nr, nc, ndr, ndc in possible_moves:
            # can't move into a wall
            if maze[nr][nc] == '#':
                continue

            # get the lowest cost to get to the next state
            lowest = lowest_cost.get((nr, nc, ndr, ndc), float("inf"))

            # if worst cost (greater) then skip
            if new_cost > lowest:
                continue

            # if better cost (less) then dump the backtrack and update the lowest cost threshold
            if new_cost < best_cost:
                lowest_cost[(nr, nc, ndr, ndc)] = new_cost

            if (nr, nc, ndr, ndc) not in backtrack:
                backtrack[(nr, nc, ndr, ndc)] = set()
            backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    # tldr; flood fill
    states = deque(end_states)
    visited = set(end_states)

    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in visited:
                continue
            visited.add(last)
            states.append(last)

    return len({(r, c) for r, c, _, _ in visited})


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/16/example1.txt', 7036),
    ('inputs/16/example2.txt', 11048),
    ('inputs/16/input.txt', 83444)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/16/example1.txt', 45),
    ('inputs/16/example2.txt', 64),
    ('inputs/16/input.txt', 483)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
