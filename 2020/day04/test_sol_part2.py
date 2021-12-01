#!/usr/bin/env python3
import re

def validate_hgt(value):
    match = re.search(r'^([0-9]+)(cm|in)$', value)
    if match is not None:
        num = int(match.groups()[0])
        unit = match.groups()[1]
        if unit == 'cm':
            return 150 <= num <= 193
        if unit == 'in':
            return 59 <= num <= 76
    else:
        return False

required_fields = {'byr','iyr','eyr','hgt','hcl','ecl','pid'} # don't care about cid
validators = {
    'byr': lambda value: re.search(r'^[0-9]{4}$', value) is not None and 1920 <= int(value) <= 2002,
    'iyr': lambda value: re.search(r'^[0-9]{4}$', value) is not None and 2010 <= int(value) <= 2020,
    'eyr': lambda value: re.search(r'^[0-9]{4}$', value) is not None and 2020 <= int(value) <= 2030,
    'hgt': lambda value: validate_hgt(value),
    'hcl': lambda value: re.search(r'^#[0-9a-f]{6}$', value) is not None,
    'ecl': lambda value: re.search(r'^amb|blu|brn|gry|grn|hzl|oth$', value) is not None,
    'pid': lambda value: re.search(r'^[0-9]{9}$', value) is not None
}
parse_field = re.compile(r'([a-z]{3}):(\S+)')


def valid_field(field, value):
    try:
        return validators[field](value)
    except KeyError:
        return False
    

def test_valid_field():
    cases = [
        ('byr', '2002', True),
        ('byr', '2003', False),
        ('hgt', '60in', True),
        ('hgt', '190cm', True),
        ('hgt', '190in', False),
        ('hgt', '190', False),
        ('hcl', '#123abc', True),
        ('hcl', '#123abz', False),
        ('hcl', '123abc', False),
        ('ecl', 'brn', True),
        ('ecl', 'wat', False),
        ('pid', '000000001', True),
        ('pid', '0123456789', False)
    ]
    for test_case in cases:
        assert valid_field(test_case[0],test_case[1]) == test_case[2]


def num_valid(filename):
    valid = 0
    with open(filename, 'r') as passports:
        fields = set()
        for line in passports.readlines():
            line = line.strip()
            if len(line) > 0:
                found_fields = parse_field.findall(line)
                for (field, value) in found_fields:
                    if valid_field(field, value):
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
    assert num_valid('example2.dat') == 4


print(num_valid('input.dat'))
