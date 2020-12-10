#!/usr/bin/env python3
import numpy as np


def calc_hops(numbers):
    a = np.sort(np.append([0], numbers))
    b = np.roll(a, -1)
    b[-1] = np.max(b) + 3
    return b - a


def calc_distri(numbers):
    c = calc_hops(numbers)
    zeros = np.sum(c == 0)
    ones = np.sum(c == 1)
    twos = np.sum(c == 2)
    threes = np.sum(c == 3)
    return zeros, ones, twos, threes


def calc_prod(numbers):
    (zeros, ones, twos, threes) = calc_distri(numbers)
    return ones * threes


def test_calc_distri():
    numbers = np.genfromtxt('example.dat')
    assert calc_prod(numbers) == 220


def gen_tribonacci():
    a = 0
    b = 1
    c = 1
    yield 1
    yield 1
    while True:
        tmp = a + b + c
        a = b
        b = c
        c = tmp
        yield tmp


class Tribonacci:
    def __init__(self):
        self.gen = gen_tribonacci()
        self.max = -1
        self.buffer = []

    def get(self, n):
        while self.max < n:
            self.buffer.append(next(self.gen))
            self.max += 1
        return self.buffer[n]



def calc_combinations(numbers):
    hops = calc_hops(numbers)
    trib = Tribonacci()
    len = 0
    agg = 1
    for hop in hops:
        if hop == 1:
            len += 1
        elif hop == 3:
            agg *= trib.get(len)
            len = 0
    return agg


def test_calc_combinations():
    numbers = np.genfromtxt('example.dat')
    assert calc_combinations(numbers) == 19208


numbers = np.genfromtxt('input.dat')
print(calc_prod(numbers))
print(calc_combinations(numbers))