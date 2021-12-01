#!/usr/bin/env python3
import re
line_format = re.compile(r'^([0-9]+)-([0-9]+) ([a-z]): (.*)$')


def valid(line):
    try:
        char, first, second, password = parse(line)
    except AttributeError:
        return False
    return bool(password[first-1] == char) ^ bool(password[second-1] == char)


def parse(line):
    match = line_format.search(line)
    first = int(match.group(1))
    second = int(match.group(2))
    char = match.group(3)
    password = match.group(4)
    return char, first, second, password


def test_valid():
    assert valid('alsdkjfasfdlkj') is False
    assert valid('aa-bb c: ccc') is False
    assert valid('1-3 b: bba UUU') is True
    assert valid('1-3 b: aaa') is False
    assert valid('1-3 b: bbb') is False
    assert valid('1-3 b: bba') is True
    assert valid('1-3 b: abb') is True


def num_valid(file_as_strs):
    nvalid = 0
    for line in file_as_strs:
        line = re.sub('\n', '', line)
        if valid(line):
            nvalid += 1
    return nvalid


def test_num_valid():
    assert num_valid(['asdfasfdadsf\n', '1-3 b: bbb\n']) == 0
    assert num_valid(['1-3 b: bba\n', '1-3 a: baa\n']) == 2


def test_example():
    assert num_valid(['1-3 a: abcde\n', '1-3 b: cdefg\n', '2-9 c: ccccccccc\n']) == 1

with open('input.dat') as data:
    lines = data.readlines()

print(num_valid(lines))
