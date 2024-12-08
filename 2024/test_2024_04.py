import pytest
from typing import List

def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines


def part1(input_file_path: str):
    lines = parse_input(input_file_path)

    return grid_word_search(lines, 'XMAS')


def grid_word_search(grid: List[List[str]], word: str) -> int:
    word_length = len(word)
    match_count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_within_bounds(x: int, y: int) -> bool:
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def is_word_match(row: int, col: int, delta_row: int, delta_col: int) -> bool:
        matched_coordinates = []
        for i in range(word_length):
            new_row, new_col = row + delta_row * i, col + delta_col * i
            if not is_within_bounds(new_row, new_col) or grid[new_row][new_col] != word[i]:
                return False
            matched_coordinates.append((new_row, new_col))
        return len(matched_coordinates) == word_length

    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == word[0]:  # Match the first letter of the word
                for delta_row, delta_col in directions:  # Explore all 8 directions
                    if is_word_match(row_index, col_index, delta_row, delta_col):
                        match_count += 1

    return match_count


def part2(input_file_path: str):
    lines = parse_input(input_file_path)
    count = 0
    coords = []
    for y in range(len(lines)):
        if 0 < y < len(lines) - 1:
            indices = [x for x, char in enumerate(lines[y]) if char == 'A']
            for x in indices:
                if 0 < x < len(lines) - 1:
                    coords.append((x, y))
    patterns = [
        ['M', 'S', 'S', 'M'],
        ['M', 'M', 'S', 'S'],
        ['S', 'M', 'M', 'S'],
        ['S', 'S', 'M', 'M'],
    ]
    for c in coords:
        for p in range(len(patterns)):
            if lines[c[1] - 1][c[0] - 1] == patterns[p][0] \
                    and lines[c[1] - 1][c[0] + 1] == patterns[p][1] \
                    and lines[c[1] + 1][c[0] + 1] == patterns[p][2] \
                    and lines[c[1] + 1][c[0] - 1] == patterns[p][3]:
                count += 1

    return count


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/04/example.txt', 18),
    ('inputs/04/input.txt', 2462)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/04/example.txt', 9),
    ('inputs/04/input.txt', 1877)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
