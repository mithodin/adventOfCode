#!/usr/bin/env python3
import numpy as np


def next_bus(active_buses, now):
    waiting_times = active_buses - (now % active_buses)
    earliest = np.argmin(waiting_times)
    return (active_buses[earliest], waiting_times[earliest])


def parse_input(filename):
    with open(filename, 'r') as f:
        now = int(f.readline().strip())
        buses = np.array([int(b) for b in f.readline().strip().split(',') if b != 'x'])
    return now, buses


def test_parse_input():
    (now, buses) = parse_input('example.dat')
    assert now == 939
    assert np.all(buses == np.array([7, 13, 59, 31, 19]))


def test_next_bus():
    (bus_id, waiting_time) = next_bus(np.array([7, 13, 59, 31, 19]), 939)
    assert bus_id == 59
    assert waiting_time == 5


(now, buses) = parse_input('input.dat')
(bus_id, waiting_time) = next_bus(buses, now)
print(bus_id, waiting_time, bus_id*waiting_time)