#!/usr/bin/env python3
import numpy as np

tree = '#'
slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]


def vector_add(v, w):
    return tuple(sum(x) for x in zip(v, w))


def trees(dx, dy, map):
    pos = (0, 0)
    num_trees = 0
    while pos[1] < len(map):
        if map[pos[1]][pos[0] % len(map[0])] == tree:
            num_trees += 1
        pos = vector_add(pos, (dx, dy))
    return num_trees


def test_trees():
    with open('example1.dat', 'r') as f:
        map = [s[:-1] for s in f.readlines()]
    assert trees(3, 1, map) == 7


def test_prod_trees():
    with open('example1.dat', 'r') as f:
        map = [s[:-1] for s in f.readlines()]
    assert np.prod([trees(slope[0], slope[1], map) for slope in slopes]) == 336
    
    
with open('input.dat', 'r') as input1:
    map = [s[:-1] for s in input1.readlines()]

print(trees(3, 1, map))
print(np.prod([trees(slope[0], slope[1], map) for slope in slopes]))


