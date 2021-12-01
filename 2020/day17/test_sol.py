#!/usr/bin/env python3
from collections import defaultdict


class Grid:
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    min_z = 0
    max_z = 0

    def __init__(self):
        self.active = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

    def sum(self):
        return sum(x for f in self.active.values() for g in f.values() for x in g.values())

    def get(self, x, y, z):
        return self.active[x][y][z]

    def set(self, x, y, z):
        self.active[x][y][z] = 1
        if x < self.min_x:
            self.min_x = x
        elif x > self.max_x:
            self.max_x = x
        if y < self.min_y:
            self.min_y = y
        elif y > self.max_y:
            self.max_y = y
        if z < self.min_z:
            self.min_z = z
        elif z > self.max_z:
            self.max_z = z

    def reset(self, x, y, z):
        self.active[x][y][z] = 0

    def active_blocks(self, x, y, z):
        active = 0
        for xx in range(x-1, x+2):
            dx = self.active[xx]
            for yy in range(y-1, y+2):
                dy = dx[yy]
                for zz in range(z-1, z+2):
                    active += dy[zz]
        return active

    def print_grid(self):
        for z in range(self.min_z, self.max_z + 1):
            print('z = {}'.format(z))
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    print('#' if self.active[x][y][z] else '.', end='')
                print('')
            print('\n')


class Game:
    active = '#'

    def __init__(self, field):
        self.grid = Grid()
        for y, line in enumerate(field):
            for x, s in enumerate(line):
                if s == self.active:
                    self.grid.set(x, y, 0)
        self.grid.print_grid()

    def turn(self):
        new_grid = Grid()
        self.grid.echo = True
        print('new turn!')
        for x in range(self.grid.min_x-1, self.grid.max_x+2):
            for y in range(self.grid.min_y - 1, self.grid.max_y + 2):
                for z in range(self.grid.min_z - 1, self.grid.max_z + 2):
                    neighbours = self.grid.active_blocks(x, y, z)
                    if self.grid.get(x, y, z) == 1:
                        if 3 <= neighbours <= 4:
                            new_grid.set(x, y, z)
                    elif neighbours == 3:
                        new_grid.set(x, y, z)
        self.grid = new_grid
        self.grid.print_grid()



def test_game():
    g = Game(['.#.', '..#', '###'])
    assert g.grid.sum() == 5
    g.turn()
    assert g.grid.sum() == 11
    g.turn()
    assert g.grid.sum() == 21
    g.turn()
    assert g.grid.sum() == 38
    g.turn()
    g.turn()
    g.turn()
    assert g.grid.sum() == 112


with open('input.dat', 'r') as f:
    g = Game([l.strip() for l in f])
for _ in range(6):
    g.turn()
print(g.grid.sum())
