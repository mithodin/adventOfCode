#!/usr/bin/env python3
from lark import Lark
import re


find_num = re.compile(r'([0-9]+)')
def parse_header(rules):
    processed_rules = []
    for rule in rules:
        if rule[:2] == '8:':
            rule = '8: 42 | 42 8'
        elif rule[:3] == '11:':
            rule = '11: 42 31 | 42 11 31'
        processed_rules.append('?{}'.format(find_num.sub(r'r\1', rule)))
    rules = '\n'.join(processed_rules)
    return Lark(rules, start='r0')


def parse_file(filename):
    with open(filename, 'r') as f:
        rules = []
        strings = []
        while (line := f.readline().strip()) != '':
            rules.append(line)
        for line in f:
            strings.append(line.strip())
    parser = parse_header(rules)
    valid = 0
    for line in strings:
        try:
            parser.parse(line)
            valid += 1
        except:
            pass
    return valid


def test_parse_file():
    assert parse_file('example2.dat') == 12


print(parse_file('input.dat'))