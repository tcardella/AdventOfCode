from collections import defaultdict, deque

import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        sections = file.read().strip().split('\n\n')
        rules = []
        for line in sections[0].splitlines():
            x, y = map(int, line.split('|'))
            rules.append([x, y])

        updates = []
        for line in sections[1].splitlines():
            updates.append(list(map(int, line.split(','))))

        return rules, updates


def part1(input_file_path: str):
    rules, updates = parse_input(input_file_path)

    return calculate_middle_sum(rules, updates)


def is_update_valid(update, rules):
    page_index = {page: i for i, page in enumerate(update)}
    for x, y in rules:
        if x in page_index and y in page_index:
            if page_index[x] > page_index[y]:
                return False
    return True


def calculate_middle_sum(rules, updates):
    valid_updates = []
    for update in updates:
        if is_update_valid(update, rules):
            valid_updates.append(update)

    middle_values = [update[len(update) // 2] for update in valid_updates]
    return sum(middle_values)


def part2(input_file_path: str):
    rules, updates = parse_input(input_file_path)

    return reorder_incorrect_updates(rules, updates)


def reorder_incorrect_updates(rules, updates):
    reordered_middle_values = []
    for update in updates:
        if not is_update_valid(update, rules):
            applicable_rules = [(x, y) for x, y in rules if x in update and y in update]
            reordered_update = topological_sort(update, applicable_rules)
            reordered_middle_values.append(reordered_update[len(reordered_update) // 2])
    return sum(reordered_middle_values)


def topological_sort(nodes, edges):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for x, y in edges:
        graph[x].append(y)
        in_degree[y] += 1
        in_degree.setdefault(x, 0)

    print(in_degree)

    zero_in_degree = deque([node for node in nodes if in_degree[node] == 0])

    sorted_order = []
    while zero_in_degree:
        node = zero_in_degree.popleft()
        sorted_order.append(node)
        for neighbour in graph[node]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                zero_in_degree.append(neighbour)

    return sorted_order


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/05/example.txt', 143),
    ('inputs/05/input.txt', 6260)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/05/example.txt', 123),
    ('inputs/05/input.txt', 5346)
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
