import functools
from collections import deque
from itertools import product

import pytest


def compute_sequences(keypad_mapping):
    pos = {}
    for r in range(len(keypad_mapping)):
        for c in range(len(keypad_mapping[r])):
            if keypad_mapping[r][c] is not None:
                pos[keypad_mapping[r][c]] = (r, c)
    sequences = {}
    for x in pos:
        for y in pos:
            if x == y:
                sequences[(x, y)] = ["A"]
                continue
            possibilities = []
            q = deque([(pos[x], "")])
            optimal = float("inf")
            while q:
                (r, c), moves = q.popleft()
                for nr, nc, nm in [(r - 1, c, "^"), (r + 1, c, "v"), (r, c - 1, "<"), (r, c + 1, ">")]:
                    if nr < 0 or nr >= len(keypad_mapping) or nc < 0 or nc >= len(keypad_mapping[nr]):
                        continue
                    if keypad_mapping[nr][nc] is None:
                        continue
                    if keypad_mapping[nr][nc] == y:
                        if optimal < len(moves) + 1:
                            break

                        optimal = len(moves) + 1
                        possibilities.append(moves + nm + "A")
                    else:
                        q.append(((nr, nc), moves + nm))
                else:
                    continue
                break
            sequences[(x, y)] = possibilities
    return sequences


numeric_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"]
]

numeric_sequences = compute_sequences(numeric_keypad)

directional_keypad = [
    [None, "^", "A"],
    ["<", "v", ">"]
]

directional_sequences = compute_sequences(directional_keypad)
directional_lengths = {key: len(value[0]) for key, value in directional_sequences.items()}


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [line.strip() for line in file.readlines()]


def solve(input_code, keypad_mapping):
    pairs = zip("A" + input_code, input_code)
    options = [keypad_mapping[(a, z)] for a, z in pairs]
    return ["".join(e) for e in product(*options)]


@functools.lru_cache(maxsize=None)
def compute_length(input_sequence, depth=25):
    if depth == 1:
        return sum(directional_lengths[(x, y)] for x, y in zip("A" + input_sequence, input_sequence))
    length = 0
    for a, z in zip("A" + input_sequence, input_sequence):
        length += min(compute_length(e, depth - 1) for e in directional_sequences[(a, z)])
    return length


def part1(input_file_path: str):
    numeric_codes = parse_input(input_file_path)
    total = 0

    for numeric_code in numeric_codes:
        possible_sequences = solve(numeric_code, numeric_sequences)
        sequence_lengths = []
        for possible_sequence in possible_sequences:
            sequence_lengths.append(compute_length(possible_sequence, 2))
        shortest_sequence_length = min(sequence_lengths)
        total += shortest_sequence_length * int(numeric_code[:-1])  # skip the last 'A' in the numeric code

    return total


def part2(input_file_path: str):
    numeric_codes = parse_input(input_file_path)
    total = 0

    for numeric_code in numeric_codes:
        possible_sequences = solve(numeric_code, numeric_sequences)
        shortest_sequence_length = min(map(compute_length, possible_sequences))
        total += shortest_sequence_length * int(numeric_code[:-1])  # skip the last 'A' in the numeric code

    return total


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/21/example.txt', 126384),
    ('inputs/21/input.txt', 125742)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/21/input.txt', 157055032722640)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
