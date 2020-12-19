#!/usr/bin/env python3
import re


def make_regex(root, rules):
    if isinstance(rules[root], str):
        return rules[root]
    return '({})'.format('|'.join('({})'.format(''.join(make_regex(sub, rules) for sub in alt)) for alt in rules[root]))


def build_regex(rules):
    return re.compile("^{}$".format(make_regex('0', rules)))


def parse_header(rules):
    parsed_rules = {}
    literal = re.compile(r'"([ab])"')
    for rule in rules:
        ex, sub = rule.split(':')
        lit = literal.findall(sub)
        if len(lit) > 0:
            parsed_rules[ex] = lit[0]
            continue
        alt = [s.strip() for s in sub.split('|')]
        parsed_rules[ex] = [tuple(subs.split(' ')) for subs in alt]
    return build_regex(parsed_rules)


def test_parse_header():
    assert parse_header(['0: "a"']).pattern == '^a$'
    assert parse_header(['0: 1 | 2', '1: "a"', '2: "b"']).pattern == '^((a)|(b))$'
    assert parse_header(['0: 1 2 | 2', '1: "a"', '2: "b"']).pattern == '^((ab)|(b))$'
    assert parse_header(['0: 1 2 | 2 2', '1: "a"', '2: "b"']).pattern == '^((ab)|(bb))$'

    pattern = parse_header(['0: 1 2', '1: "a"', '2: 1 3 | 3 1', '3: "b"'])
    assert pattern.match("aab") is not None
    assert pattern.match("aba") is not None
    assert pattern.match("aaa") is None


def parse_file(filename):
    with open(filename, 'r') as f:
        rules = []
        strings = []
        while (line := f.readline().strip()) != '':
            rules.append(line)
        for line in f:
            strings.append(line.strip())
    pattern = parse_header(rules)
    valid = 0
    for line in strings:
        if pattern.match(line) is not None:
            valid += 1
    return valid


def test_parse_file():
    assert parse_file('example.dat') == 2


print(parse_file('input.dat'))