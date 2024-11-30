import os

import pytest


class Day01:
    def part1(self, input_file_path: str):
        with open(os.path.join(os.getcwd(), input_file_path), 'r') as file:
            inputs = file.readlines()

    def part2(self, input_file_path: str):
        with open(os.path.join(os.getcwd(), input_file_path), 'r') as file:
            inputs = file.readlines()

@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/01/example1.txt', 142),
    ('inputs/01/input.txt', 56465)
])
def part1(input_file_path, expected):
    assert expected == expected

@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/01/example1.txt', 142),
    ('inputs/01/input.txt', 56465)
])
def part2(input_file_path, expected):
    assert expected == expected