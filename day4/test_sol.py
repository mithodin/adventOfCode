#!/usr/bin/env python3
import re

required_fields = {'byr','iyr','eyr','hgt','hcl','ecl','pid'} # don't care about cid
valid_field = re.compile(r'([a-z][a-z][a-z]):(\S+)')

def num_valid(filename):
    valid = 0
    with open(filename, 'r') as passports:
        fields = set()
        for line in passports.readlines():
            line = line.strip()
            if len(line) > 0:
                found_fields = valid_field.findall(line)
                for (field, value) in found_fields:
                    fields.add(field)
            else:
                if fields.issuperset(required_fields):
                    valid += 1
                fields = set()
    if not len(fields) == 0:
        if fields.issuperset(required_fields):
            valid += 1
    return valid


def test_num_valid():
    assert num_valid('example.dat') == 2

print(num_valid('input.dat'))
