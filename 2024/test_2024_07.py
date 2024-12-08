import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        output = []
        for e in [line.split(':') for line in
                  [line.strip() for line in file.readlines()]]:
            test_values = map(int, e[1].split())
            output.append((int(e[0]), list(test_values)))

        return output


def evaluate_left_to_right(numbers, operators):
    value = numbers[0]
    for num, op in zip(numbers[1:], operators):
        if op == '*':
            value *= num
        elif op == '+':
            value += num
        elif op == '||':
            value = int(str(value) + str(num))

    return value


def generate_operator_combinations(numbers, current_ops, all_ops, valid_ops):
    if len(current_ops) == len(numbers) - 1:
        all_ops.append(current_ops.copy())
        return

    for op in valid_ops:
        current_ops.append(op)
        generate_operator_combinations(numbers, current_ops, all_ops, valid_ops)
        current_ops.pop()


def get_valid_calibrations(calibrations, valid_ops):
    valid_results = []

    for result, numbers in calibrations:
        all_operator_combinations = []
        generate_operator_combinations(numbers, [], all_operator_combinations, valid_ops)

        for ops in all_operator_combinations:
            if evaluate_left_to_right(numbers, ops) == result:
                valid_results.append(result)
                break

    return sum(valid_results)


def part1(input_file_path: str):
    calibration_equations = parse_input(input_file_path)
    return get_valid_calibrations(calibration_equations, ['*', '+'])


def part2(input_file_path: str):
    calibration_equations = parse_input(input_file_path)
    return get_valid_calibrations(calibration_equations, ['*', '+', '||'])


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/07/example.txt', 3749),
    ('inputs/07/input.txt', 6083020304036)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/07/example.txt', 11387),
    ('inputs/07/input.txt', 59002246504791)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
