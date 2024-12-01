import os
from functools import reduce
from operator import mul

import pytest


class Day02:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = os.path.join(script_dir, 'inputs/02')

    def part1(self, input_file_path: str):
        with open(os.path.join(self.input_dir, input_file_path), 'r') as file:
            inputs = file.readlines()

        available_cubes = {"red": 12, "green": 13, "blue": 14}
        total_sum = 0

        for input_line in inputs:
            line = input_line.strip().split(':')
            game_number = int(line[0].split(' ')[-1])
            game_description = line[-1]

            cube_dict = self.parse_cube_set(game_description)
            is_valid = all(available_cubes[cube] >= count for cube, count in cube_dict.items())

            if is_valid:
                total_sum += game_number

        return total_sum

    def part2(self, input_file_path: str):
        with open(os.path.join(self.input_dir, input_file_path), 'r') as file:
            inputs = file.readlines()

        total_sum = 0

        for input_line in inputs:
            line = input_line.strip().split(':')
            game_description = line[-1]

            cube_dict = self.parse_cube_set(game_description)
            aggregate = reduce(mul, cube_dict.values(), 1)  # Multiply all values in the dictionary
            total_sum += aggregate

        return total_sum

    def parse_cube_set(self, game_description):
        cube_dict = {}
        sets = game_description.split(';')

        for set_ in sets:
            cubes = {
                cube.split(' ')[1]: int(cube.split(' ')[0])
                for cube in map(str.strip, set_.split(','))
            }

            for cube, value in cubes.items():
                if cube not in cube_dict:
                    cube_dict[cube] = value
                else:
                    cube_dict[cube] = max(cube_dict[cube], value)

        return cube_dict

@pytest.mark.parametrize('input_file_path, expected', [
    ('example.txt', 8),
    ('input.txt', 2156)
])
def test_part_1(input_file_path, expected):
    day01 = Day02()
    actual = day01.part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('example.txt', 2286),
    ('input.txt', 66909)
])
def test_part_2(input_file_path, expected):
    day02 = Day02()
    actual = day02.part2(input_file_path)
    assert actual == expected
