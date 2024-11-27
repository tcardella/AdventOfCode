import sys

import pytest


class Day01:
    def part1(self, input_file_path: str):
        with open(input_file_path, 'r') as file:
            inputs = file.readlines()

        tokens = "1|2|3|4|5|6|7|8|9".split('|')

        total_sum = 0

        for input_line in inputs:
            output_tokens = [char for char in input_line if char in tokens]

            value = int(f"{output_tokens[0]}{output_tokens[-1]}")

            total_sum += value

        return total_sum

    def part2(self, input_file_path: str):
        with open(input_file_path, 'r') as file:
            inputs = file.readlines()

        total_sum = 0

        tokens = "1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine".split('|')

        for input_line in inputs:
            input_line = input_line.strip()

            first_idx = sys.maxsize
            first_token = ''

            last_idx = -1
            last_token = ''

            for token in tokens:
                f_idx = input_line.find(token)
                rf_idx = input_line.rfind(token)

                if f_idx >= 0 or rf_idx >= 0:
                    if first_idx > f_idx:
                        first_idx = f_idx
                        first_token = token

                    if last_idx < rf_idx:
                        last_idx = rf_idx
                        last_token = token

            if not first_token.isdigit():
                first_token = tokens[first_token]

            if not last_token.isdigit():
                last_token = tokens[last_token]

            value = int(f"{first_token}{last_token}")
            total_sum += value

        return total_sum


@pytest.mark.parametrize('input_file_path, expected', [
    ('../inputs/01/example1.txt', 142),
    ('../inputs/01/input.txt', 56465)
])
def test_part1(input_file_path, expected):
    day01 = Day01()
    actual = day01.part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('../inputs/01/example2.txt', 281),
    ('../inputs/01/input.txt', 55902)
])
def test_part_2(input_file_path, expected):
    day01 = Day01()
    actual = day01.part2(input_file_path)
    assert actual == expected
