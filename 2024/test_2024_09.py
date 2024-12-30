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
    output = []
    file_id = 0

    for i, e in enumerate(disk_map):
        x = int(e)
        if i % 2 == 0:
            output += [file_id] * x
            file_id += 1
        else:
            output += [-1] * x

    return output


def defragment(disk_map):
    blanks = [i for i, e in enumerate(disk_map) if e == -1]

    for i in blanks:
        while disk_map[-1] == -1:
            disk_map.pop()
        if len(disk_map) <= i:
            break
        disk_map[i] = disk_map.pop()

    return disk_map


def calculate_checksum(disk_map):
    return sum(i * e for i, e in enumerate(disk_map))


def calculate_checksum2(files):
    checksum = 0
    for file_id, (pos, size) in files.items():
        for e in range(pos, pos + size):
            checksum += e * file_id
    return checksum


def part2(input_file_path: str):
    disk_map = parse_input(input_file_path)
    files = defragment2(disk_map)
    return calculate_checksum2(files)


def defragment2(disk_map):
    files = {}
    blanks = []

    file_id = 0
    pos = 0

    for i, e in enumerate(disk_map):
        x = int(e)
        if i % 2 == 0:
            files[file_id] = (pos, x)
            file_id += 1
        else:
            if x != 0:
                blanks.append((pos, x))
        pos += x

    while file_id > 0:
        file_id -= 1
        pos, size = files[file_id]
        for i, (start, length) in enumerate(blanks):
            if start >= pos:
                blanks = blanks[:i]
                break
            if size <= length:
                files[file_id] = (start, size)
                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)
                break

    return files


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
