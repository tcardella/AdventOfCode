import pytest


def parse_input(input_file_path: str):
    with open(input_file_path, 'r', encoding="utf-8-sig") as file:
        return [line.strip().split('-') for line in file.readlines()]


def build_graph(connections):
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def part1(input_file_path: str):
    connections = parse_input(input_file_path)
    graph = build_graph(connections)

    triples = set()
    for a in graph:
        for b in graph[a]:
            for c in graph[b]:
                if a != c and a in graph[c]:
                    triples.add(tuple(sorted([a, b, c])))

    count = 0
    for triple in triples:
        if any(e.startswith('t') for e in triple):
            count += 1

    return count


def part2(input_file_path: str):
    connections = parse_input(input_file_path)
    graph = build_graph(connections)

    sets = set()

    def search(node, required_nodes):
        key = tuple(sorted(required_nodes))
        if key in sets: return
        sets.add(key)
        for neighbor in graph[node]:
            if neighbor in required_nodes:
                continue
            if not all(neighbor in graph[query] for query in required_nodes):
                continue
            search(neighbor, {*required_nodes, neighbor})

    for e in graph:
        search(e, {e})

    return ",".join(sorted(max(sets, key=len)))


@pytest.mark.parametrize("input_file_path, expected", [
    ('inputs/23/example.txt', 7),
    ('inputs/23/input.txt', 1175)
])
def test_part_1(input_file_path, expected):
    actual = part1(input_file_path)
    assert actual == expected


@pytest.mark.parametrize('input_file_path, expected', [
    ('inputs/23/example.txt', 'co,de,ka,ta'),
    ('inputs/23/input.txt', 'bw,dr,du,ha,mm,ov,pj,qh,tz,uv,vq,wq,xw')
])
def test_part_2(input_file_path, expected):
    actual = part2(input_file_path)
    assert actual == expected
