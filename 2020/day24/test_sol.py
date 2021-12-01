#!/usr/bin/env python3
import re
from collections import defaultdict
from functools import reduce


def vadd(x, y):
    return x[0] + y[0], x[1] + y[1]


parse_path = re.compile(r'(e|se|sw|w|nw|ne)')
vectors = {
    'e': (1,0),
    'se': (1,-1),
    'sw': (0,-1),
    'w': (-1,0),
    'nw': (-1,1),
    'ne': (0,1)
}
def build_pattern(paths):
    grid = defaultdict(lambda: False)
    for path in paths:
        pos = (0, 0)
        for step in parse_path.findall(path):
            pos = vadd(pos,vectors[step])
        grid[pos] = not grid[pos]
    return grid


def count_black(grid):
    return sum(grid.values())


def load_paths(filename):
    with open(filename, 'r') as f:
        paths = [s.strip() for s in f]
    return paths


def test_build_pattern():
    num_black = count_black(build_pattern(['nwwswee']))
    assert num_black == 1

    num_black = count_black(build_pattern(load_paths('example.dat')))
    assert num_black == 10


def count_around(x,y, grid):
    count = 0
    for direction in vectors.values():
        if grid[vadd((x,y), direction)]:
            count += 1
    return count


def run_game(grid, turns):
    min_x,max_x,min_y,max_y = reduce(lambda current, next: (min(current[0],next[0]),max(current[1],next[0]),min(current[2],next[1]),max(current[3],next[1])), (x for x in grid.keys()), (0,0,0,0))
    for _ in range(turns):
        new_grid = defaultdict(lambda: False)
        min_x -= 1
        max_x += 1
        min_y -= 1
        max_y += 1
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                count = count_around(x, y, grid)
                black = grid[(x,y)]
                if (black and 1 <= count <= 2) or (not black and count == 2):
                    new_grid[x,y] = True
        grid = new_grid
    return grid


def test_run_game():
    grid = build_pattern(load_paths('example.dat'))
    grid = run_game(grid, 1)
    assert count_black(grid) == 15
    grid = run_game(grid, 1)
    assert count_black(grid) == 12
    grid = run_game(grid, 1)
    assert count_black(grid) == 25
    grid = run_game(grid, 1)
    assert count_black(grid) == 14
    grid = run_game(grid, 1)
    assert count_black(grid) == 23
    grid = run_game(grid, 95)
    assert count_black(grid) == 2208

pattern = build_pattern(load_paths('input.dat'))
print(count_black(pattern))
grid = run_game(pattern, 100)
print(count_black(grid))