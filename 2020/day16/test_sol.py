#!/usr/bin/env python3
import re
import numpy as np


def make_rule(bounds):
    return lambda x: bounds[0][0] <= x <= bounds[0][1] or bounds[1][0] <= x <= bounds[1][1]


rule_parser = re.compile(r'^([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$')
def make_rules(lines):
    rules = {}
    for line in lines:
        name, r0_lower, r0_upper, r1_lower, r1_upper = rule_parser.findall(line)[0]
        r0_lower = int(r0_lower)
        r0_upper = int(r0_upper)
        r1_lower = int(r1_lower)
        r1_upper = int(r1_upper)
        rules[name] = make_rule(((r0_lower, r0_upper),(r1_lower,r1_upper)))
    return rules


def test_make_rules():
    rules = make_rules(["a: 1-2 or 4-5"])
    assert rules['a'](1) is True
    assert rules['a'](3) is False
    assert rules['a'](5) is True


def invalid_numbers(rules, numbers):
    return [x for x in numbers if np.all([not valid(x) for valid in rules.values()])]


def test_invalid_numbers():
    rules = make_rules(['a: 1-2 or 4-5', 'b: 5-10 or 11-20'])
    invalid = invalid_numbers(rules, [1,2,3,4,5,6])
    assert invalid == [3]


def parse_input(filename):
    rules = []
    with open(filename, 'r') as f:
        while (line := f.readline().strip()) != '':
            rules.append(line)
        f.readline()
        my_ticket = [int(x) for x in f.readline().strip().split(',')]
        f.readline()
        f.readline()
        nearby_tickets = [[int(x) for x in s.strip().split(',')] for s in f.readlines()]
    return make_rules(rules), my_ticket, nearby_tickets


def test_rules():
    rules, my_ticket, nearby_tickets = parse_input('example.dat')
    invalid = [n for numbers in nearby_tickets for n in invalid_numbers(rules, numbers)]
    assert invalid == [4, 55, 12]
    assert sum(invalid) == 71


rules, my_ticket, nearby_tickets = parse_input('input.dat')
invalid = [n for numbers in nearby_tickets for n in invalid_numbers(rules, numbers)]
print(sum(invalid))

def valid_rules(rules, numbers):
    return {rule for rule in rules if np.all([rules[rule](x) for x in numbers])}


def test_valid_rules():
    rules = make_rules(['a: 1-2 or 4-5', 'b: 5-10 or 11-20'])
    assert valid_rules(rules, [1, 2, 4]) == {'a'}
    assert valid_rules(rules, [6, 7, 15]) == {'b'}
    assert valid_rules(rules, [5, 5, 5]) == {'a', 'b'}


def find_matching_rules(rules, valid_tickets):
    options = [(n, valid_rules(rules, valid_tickets[:, n])) for n in range(valid_tickets.shape[1])]
    options = sorted(options, key=lambda elem: len(elem[1]))
    res = rec_find(options, set())
    return res


def rec_find(options, found):
    if len(options) == 0:
        return dict()
    my_options = options[0][1] - found
    column = options[0][0]
    if len(my_options) == 0:
        return None
    for opt in my_options:
        res = rec_find(options[1:], found | {opt})
        if res is not None:
            res[column] = opt
            return res


def test_find_matching_rules():
    rules, my_ticket, nearby_tickets = parse_input('example2.dat')
    valid_nearby_tickets = np.array([numbers for numbers in nearby_tickets if len(invalid_numbers(rules, numbers)) == 0])
    res = find_matching_rules(rules, valid_nearby_tickets)
    assert res == {0: 'row', 1: 'class', 2: 'seat'}

valid_nearby_tickets = np.array([numbers for numbers in nearby_tickets if len(invalid_numbers(rules, numbers)) == 0])
labels = find_matching_rules(rules, valid_nearby_tickets)
print(labels)

prod_vals = 1
for k, val in enumerate(my_ticket):
    print('{}: {}'.format(labels[k], val))
    if labels[k][:9] == 'departure':
        prod_vals *= val
print(prod_vals)


