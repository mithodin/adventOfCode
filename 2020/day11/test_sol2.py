#!/usr/bin/env python3
import numpy as np


seat = 'L'
occupied_seat = '#'


def load_file(filename):
    with open(filename, 'r') as f:
        return np.array([[c for c in s.strip()] for s in f]).T


def seeing_occupied_seat(seats):
    if len(seats) < 2:
        return False
    seeing = seats[1:]
    try:
        first_occupied = np.where(seeing == occupied_seat)[0][0]
    except IndexError:
        return False
    try:
        first_unoccupied = np.where(seeing == seat)[0][0]
    except IndexError:
        return True
    return first_occupied < first_unoccupied


def occupied_seats_around(x, y, seats):
    dims = seats.shape
    nl = seeing_occupied_seat(seats[x::-1, y])
    nr = seeing_occupied_seat(seats[x:, y])
    nu = seeing_occupied_seat(seats[x, y::-1])
    nd = seeing_occupied_seat(seats[x, y:])
    n_diag = y - x
    i_diag = x if n_diag > 0 else y
    diag = seats.diagonal(n_diag)
    ndu = seeing_occupied_seat(diag[i_diag::-1])
    ndd = seeing_occupied_seat(diag[i_diag:])
    flipped = np.fliplr(seats)
    y = dims[1] - y - 1
    n_diag = y - x
    i_diag = x if n_diag > 0 else y
    diag = flipped.diagonal(n_diag)
    nodu = seeing_occupied_seat(diag[i_diag::-1])
    nodd = seeing_occupied_seat(diag[i_diag:])
    return 0 + nl + nr + nu + nd + ndu + ndd + nodu + nodd


def test_occupied_seats_around():
    seats = load_file('example2_1.dat')
    assert occupied_seats_around(0, 0, seats) == 3
    assert occupied_seats_around(1, 7, seats) == 6


def iterate(seats):
    dims = seats.shape
    next_seats = np.copy(seats)
    for x in range(0, dims[0]):
        for y in range(0, dims[1]):
            if seats[x, y] == seat or seats[x, y] == occupied_seat:
                num_around = occupied_seats_around(x, y, seats)
                next_seats[x, y] = occupied_seat if num_around == 0 else seat if num_around >= 5 else seats[x, y]
    return next_seats


def gen_iterations(seats):
    yield seats
    while True:
        seats = iterate(seats)
        yield seats


def test_gen_iterations():
    initial = load_file('example2_0.dat')
    gen = gen_iterations(initial)
    for i in range(0, 7):
        nx = next(gen)
        print(nx.T)
        assert np.all(nx == load_file('example2_{:.0f}.dat'.format(i)))
    for i in range(2):
        assert np.all(next(gen) == load_file('example2_6.dat'))


def find_stable(seats):
    gen = gen_iterations(seats)
    prev = next(gen)
    while not np.all((next_seats := next(gen)) == prev):
        prev = next_seats
    return prev


def test_find_stable():
    initial = load_file('example2_0.dat')
    assert np.all(find_stable(initial) == load_file('example2_6.dat'))


seats = load_file('input.dat')
print(np.sum(find_stable(seats) == occupied_seat))

