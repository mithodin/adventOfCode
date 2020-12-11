#!/usr/bin/env python3
import re
line_format = re.compile(r'^([0-9]+)-([0-9]+) ([a-z]): (.*)$')


def valid(line):
    try:
        char, lower, password, upper = parse(line)
    except AttributeError:
        return False
    if upper < lower:
        return False
    num_char = len(re.findall(char, password))
    return lower <= num_char <= upper


def parse(line):
    match = line_format.search(line)
    lower = int(match.group(1))
    upper = int(match.group(2))
    char = match.group(3)
    password = match.group(4)
    return char, lower, password, upper


def test_valid():
    assert valid('alsdkjfasfdlkj') is False
    assert valid('aa-bb c: ccc') is False
    assert valid('2-1 b: aaa') is False
    assert valid('1-3 b: aaa') is False
    assert valid('1-3 b: bba') is True


def num_valid(file_as_strs):
    nvalid = 0
    for line in file_as_strs:
        line = re.sub('\n', '', line)
        if valid(line):
            nvalid += 1
    return nvalid


def test_num_valid():
    assert num_valid(['asdfasfdadsf\n', '1-3 b: bbb\n']) == 1
    assert num_valid(['1-3 b: bbb\n', '1-3 a: aaa\n']) == 2


def test_example():
    assert num_valid(['1-3 a: abcde\n', '1-3 b: cdefg\n', '2-9 c: ccccccccc\n']) == 2


with open('input.dat') as data:
    lines = data.readlines()

print(num_valid(lines))
