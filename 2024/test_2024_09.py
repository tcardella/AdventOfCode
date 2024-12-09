import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return file.read().strip()


def part1(input_file_path: str):
    disk_map = parse_input(input_file_path)
    disk_map = decompress(disk_map)
    disk_map = defragment(disk_map)
    return calculate_checksum(disk_map)


def decompress(disk_map):
    file_id = 0
    output = []
    for i, e in enumerate(disk_map):
        if i % 2 == 0:
            for idx in range(int(disk_map[i])):
                output.append(file_id)
            file_id += 1
        else:
            for idx in range(int(disk_map[i])):
                output.append('.')

    return output


def find_first_gap(s):
    for i in range(len(s)):
        if s[i] == '.':
            return i


def find_last_value(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i] != '.':
            return i


def swap(s, a, b):
    s[a], s[b] = s[b], s[a]


def defragment(disk_map):
    start = find_first_gap(disk_map)
    end = find_last_value(disk_map)

    while start < end:
        swap(disk_map, start, end)
        start = find_first_gap(disk_map)
        end = find_last_value(disk_map)

    return disk_map


def calculate_checksum(disk_map):
    checksum = 0
    for i, e in enumerate(disk_map):
        if e == '.':
            return checksum
        checksum += i * int(e)
    return checksum


def swap_chunks(s, space_start, space_end, value_start, value_end):
    spaces = [e for e in range(space_start, space_end + 1)]
    values = [e for e in range(value_start, value_end + 1)]
    for e in list(zip(spaces, values)):
        swap(s, e[0], e[1])


def defragment2(disk_map):
    unique_file_ids = list(reversed(list(set([i for i in disk_map if i != '.']))))

    for file_id in unique_file_ids:
        file_block = get_file_block(disk_map, file_id)
        spaces = get_spaces(disk_map[:file_block[0]])
        file_block_size = file_block[1] - file_block[0] + 1

        for space in spaces:
            avail_space = space[1] - space[0] + 1
            if avail_space >= file_block_size:
                swap_chunks(disk_map, space[0], space[1], file_block[0], file_block[1])
                break

    return disk_map


def part2(input_file_path: str):
    disk_map = parse_input(input_file_path)
    disk_map = decompress(disk_map)
    disk_map = defragment2(disk_map)
    return calculate_checksum(disk_map)


def get_spaces(disk_map):
    sequences = []
    start = None

    for i, char in enumerate(disk_map):
        if char == '.' and start is None:
            # Start of a new sequence of dots
            start = i
        elif char != '.' and start is not None:
            # End of a sequence of dots
            sequences.append((start, i - 1))
            start = None

    # Make sure to capture if the last part of the string is a dot sequence
    if start is not None:
        sequences.append((start, len(disk_map) - 1))

    return sequences


def get_file_block(disk_map, file_id):
    a = [(i, e) for i, e in enumerate(disk_map)]
    b = [(i, e) for i, e in a if e == file_id]
    return b[0][0], b[-1][0]


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/09/example.txt', 1928),
    ('inputs/09/input.txt', 6360094256423)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/09/example.txt', 2858),
    ('inputs/09/input.txt', 6379677752410)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
