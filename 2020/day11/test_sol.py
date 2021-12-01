#!/usr/bin/env python3
import numpy as np


seat = 'L'
occupied_seat = '#'


def load_file(filename):
    with open(filename, 'r') as f:
        return np.array([[c for c in s.strip()] for s in f])


def occupied_seats_around(x, y, seats):
    dims = seats.shape
    return np.sum(seats[max(x-1, 0):min(x+2, dims[0]), max(y-1, 0):min(y+2, dims[1])] == occupied_seat) - (seats[x, y] == occupied_seat)


def iterate(seats):
    dims = seats.shape
    next_seats = np.copy(seats)
    for x in range(0, dims[0]):
        for y in range(0, dims[1]):
            if seats[x, y] == seat or seats[x, y] == occupied_seat:
                num_around = occupied_seats_around(x, y, seats)
                next_seats[x, y] = occupied_seat if num_around == 0 else seat if num_around >= 4 else seats[x, y]
    return next_seats


def gen_iterations(seats):
    yield seats
    while True:
        seats = iterate(seats)
        yield seats


def test_gen_iterations():
    initial = load_file('example_0.dat')
    gen = gen_iterations(initial)
    for i in range(0, 6):
        assert np.all(next(gen) == load_file('example_{:.0f}.dat'.format(i)))
    for i in range(2):
        assert np.all(next(gen) == load_file('example_5.dat'))


def find_stable(seats):
    gen = gen_iterations(seats)
    prev = next(gen)
    while not np.all((next_seats := next(gen)) == prev):
        prev = next_seats
    return prev


def test_find_stable():
    initial = load_file('example_0.dat')
    assert np.all(find_stable(initial) == load_file('example_5.dat'))


seats = load_file('input.dat')
print(np.sum(find_stable(seats) == occupied_seat))

