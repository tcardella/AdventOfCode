import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return file.read().strip()


def part1(input_file_path: str):
    disk_map = parse_input(input_file_path)

    decompressed_disk_map = decompress(disk_map)
    defragmented_disk_map = defragment(decompressed_disk_map)
    return calculate_checksum(defragmented_disk_map)


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


def defragment(decompressed_disk_map):
    s = decompressed_disk_map

    start = find_first_gap(s)
    end = find_last_value(s)

    while start < end:
        swap(s, start, end)
        start = find_first_gap(s)
        end = find_last_value(s)

    return s


def calculate_checksum(s):
    checksum = 0
    for i, e in enumerate(s):
        if e == '.':
            return checksum
        checksum += i * int(e)
    return checksum


def calculate_checksum2(s):
    checksum = 0
    for i, e in enumerate(s):
        if e == '.':
            continue
        checksum += i * int(e)
    return checksum


def find_first_gap_of_length(s, target_size):
    start = 0
    end = 0
    for i in range(len(s)):
        if s[i - 1] != '.' and s[i] == '.':
            start = i
        if s[i - 1] == '.' and s[i] != '.':
            end = i
            if end - start < target_size:
                continue
            else:
                return start, end
    return start, len(s)


def find_last_values(s):
    start = len(s)
    end = len(s)
    last_val = s[-1]
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '.' and s[i] == last_val:
            end -= 1
            start -= 1

        elif s[i] != '.' and s[i] == last_val:
            start -= 1

        elif s[i] != '.' and s[i] != last_val:
            break

        elif s[i] == '.' and s[i] != last_val:
            break

        last_val = s[i]

    return start, end


# @pytest.mark.parametrize('s', [
#     '00...111...2...333.44.5555.6666.777.888899'
# ])
# def test_find_last_values(s):
#     # Calculate and print the checksum
#     checksum = calculate_checksum(list(s))
#     print("Checksum:", checksum)

# actual = find_last_values(s)
# print(actual)
# assert actual == (40, 42)
# actual = find_last_values(s[:actual[0]])
# print(actual)
# assert actual == (36, 40)


def swap_chunks(s, g_start, g_end, v_start, v_end):
    gaps = [e for e in range(g_start, g_end + 1)]
    values = [e for e in range(v_start, v_end + 1)]
    x = list(zip(gaps, values))
    for e in x:
        swap(s, e[0], e[1])


def defragment2(s):
    def find_file_spans(s):
        spans = {}
        current_char = s[0]
        start = 0

        for i, e in enumerate(s):
            if e != current_char:
                if current_char != '.':
                    spans[current_char] = (start, i)  # end is non-inclusive
                start = i
                current_char = e
        if current_char != '.':
            spans[current_char] = (start, len(s))

        return sorted(spans.items(), key=lambda x: int(x[0]), reverse=True)  # Sort by file ID descending

    def find_free_spans(s):
        free_spans = []
        start = None
        for i, e in enumerate(s):
            if e == '.' and start is None:
                start = i
            elif e != '.' and start is not None:
                free_spans.append((start, i))
                start = None
        if start is not None:  # Handle trailing free space
            free_spans.append((start, len(s)))
        return free_spans

    file_spans = find_file_spans(s)
    free_spans = find_free_spans(s)

    for file, (v_start, v_end) in file_spans:
        file_size = v_end - v_start
        # Look for the first suitable free span that can fit the file
        for i, (g_start, g_end) in enumerate(free_spans):
            if g_end - g_start >= file_size:
                # Move file to this free span
                s[g_start:g_start + file_size] = s[v_start:v_end]
                s[v_start:v_end] = ['.'] * file_size
                # Update free spans; split if necessary
                free_spans[i] = (g_start + file_size, g_end)
                break  # Move to the next file

    return s


def part2(input_file_path: str):
    disk_map = parse_input(input_file_path)
    disk_map = decompress(disk_map)

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

    # print(disk_map)

    # defragmented_disk_map = defragment2(decompressed_disk_map)
    return calculate_checksum2(disk_map)


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
