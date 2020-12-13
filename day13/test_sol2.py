#!/usr/bin/env python3
def parse_input(filename):
    with open(filename, 'r') as f:
        _ = int(f.readline().strip())
        buses_raw = f.readline().strip().split(',')
        bus0 = int(buses_raw[0])
        buses = {int(b): i for i, b in enumerate(buses_raw) if b != 'x'}
    return (bus0, buses)


def test_parse_input():
    (bus0, buses) = parse_input('example.dat')
    assert bus0 == 7
    assert buses == {7:0, 13:1, 59:4, 31:6, 19:7}


def calc_coefficient(n, k, delta):
    if n == 1:
        return 0
    for i in range(1, k):
        if (n * i + delta) % k == 0:
            return i


def test_calc_coefficients():
    assert calc_coefficient(2, 3, 1) == 1
    assert calc_coefficient(7, 13, 1) == 11
    assert calc_coefficient(2, 6, 1) is None
    assert calc_coefficient(1, 2, 0) == 0


def find_departure(bus0, rules):
    other_buses = list(rules.keys())
    other_buses.remove(bus0)
    return find_min_multiple(1, bus0, lambda x: x, other_buses, rules)


def find_min_multiple(bus0, bus1, delta, buses, rules):
    d = delta(0)
    coeff = calc_coefficient(bus0, bus1, d + rules[bus1])
    if len(buses) == 0:
        return coeff
    return (coeff + bus1 * find_min_multiple(bus0 * bus1, buses[0], lambda x: delta(coeff + bus1 * x), buses[1:], rules))


def test_find_min_multiple():
    buses = [3]
    rules = {2: 0, 3: 1}
    assert find_min_multiple(1, 2, lambda x: x, buses, rules) == 2


def test_find_departure():
    assert find_departure(2, {2:0, 3:1, 5:2}) == 8
    assert find_departure(2, {2:0, 3:1, 5:2, 7:3}) == 158
    assert find_departure(17, {17:0, 13:2, 19:3}) == 3417
    assert find_departure(67, {67:0, 7:1, 59:2, 61:3}) == 754018
    assert find_departure(67, {67:0, 7:2, 59:3, 61:4}) == 779210
    assert find_departure(67, {67:0, 7:1, 59:3, 61:4}) == 1261476
    assert find_departure(1789, {1789:0, 37:1, 47:2, 1889: 3}) == 1202161486


(bus0, rules) = parse_input('input.dat')
print(find_departure(bus0, rules))
