#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import reduce


def map_unsafe_ingredients(tags):
    max = 2
    while max > 1:
        max = 1
        identified = set(list(s)[0] for s in tags.values() if len(s) == 1)
        for tag in tags.keys():
            size = len(tags[tag])
            if size > max:
                max = size
            if size > 1:
                tags[tag] -= identified
    mapped = {list(tags[t])[0]: t for t in tags.keys()}
    return mapped


def parse_list(lines):
    pattern = re.compile(r'(([a-z]+ )+)\(contains ([a-z]+(, [a-z]+)*)\)')
    ingredients = set()
    tag = defaultdict(lambda: set() | ingredients)
    counts = defaultdict(lambda: 0)
    for line in lines:
        ingr, _, tags, _ = pattern.findall(line)[0]
        ingr = set(ingr.strip().split(' '))
        for i in ingr:
            counts[i] += 1
        tags = set(tags.split(', '))
        ingredients |= ingr
        for t in tags:
            tag[t] &= ingr
    maybe_unsafe = reduce(lambda ini, nx: ini | nx, tag.values(), set())
    safe = ingredients - maybe_unsafe
    num_safe = reduce(lambda ini, n: ini + counts[n], safe, 0)
    unsafe_mapped = map_unsafe_ingredients(tag)
    return safe, num_safe, unsafe_mapped


def test_parse_list():
    unsafe_ones = {
        'mxmxvkd': 'dairy',
        'sqjhc': 'fish',
        'fvjkl': 'soy'
    }
    safe_ones = {'kfcds', 'nhms', 'sbzzf', 'trh'}
    num_safe_ones = 5
    with open('example.dat', 'r') as f:
        safe, num_safe, unsafe = parse_list(l.strip() for l in f)
    assert safe.issubset(safe_ones) and safe.issuperset(safe_ones)
    assert num_safe == num_safe_ones
    assert unsafe == unsafe_ones


with open('input.dat', 'r') as f:
    safe, num_safe, unsafe = parse_list(l.strip() for l in f)
    print(','.join(t[0] for t in sorted(((k, unsafe[k]) for k in unsafe.keys()), key=lambda t: t[1])))
    print(num_safe)