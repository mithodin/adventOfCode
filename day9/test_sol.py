#!/usr/bin/env python3
import numpy as np


def calc_sums(numbers):
    c = numbers.reshape([1, -1])+numbers.reshape([-1, 1])
    np.fill_diagonal(c, 0)
    return c


def valid_xmas(numbers, preamble):
    buffer = numbers[:preamble]
    for i, number in enumerate(numbers[preamble:]):
        valid = np.any(calc_sums(buffer) == number)
        if not valid:
            return number
        buffer[i % preamble] = number


def test_valid_xmas():
    numbers = np.genfromtxt('example.dat', dtype='int')
    assert valid_xmas(numbers, 5) == 127


data = np.genfromtxt('input.dat', dtype='int64')
invalid = valid_xmas(data, 25)
print(invalid)


def gen_continguous_sets(numbers):
    for length in range(2, len(numbers)):
        for start in range(len(numbers)-length):
            yield numbers[start:start+length]


def find_sum(target, numbers):
    for test_set in gen_continguous_sets(numbers):
        if np.sum(test_set) == target:
            return np.min(test_set) + np.max(test_set)


def test_find_sum():
    numbers = np.genfromtxt('example.dat', dtype='int')
    assert find_sum(127, numbers) == 62


print(find_sum(invalid, data))
