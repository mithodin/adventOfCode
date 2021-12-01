#!/usr/bin/env python3
from collections import defaultdict

import numpy as np
import re


def invert_signature(sig, length):
    return int("{{:0{}b}}".format(length).format(sig)[-1::-1], 2)


def border_to_signature(border):
    return sum(2**i for i, c in enumerate(border) if c == '#')


def test_border_to_signature():
    assert border_to_signature(np.array(['#', '.', '.', '#'])) == 9
    assert border_to_signature(np.array(['.', '.', '.', '.', '#'])) == 16


def get_border_signatures(tile):
    b0 = border_to_signature(tile[:, -1])
    b1 = border_to_signature(tile[0, :])
    b2 = border_to_signature(tile[-1::-1, 0])
    b3 = border_to_signature(tile[-1, -1::-1])
    return b0, b1, b2, b3


def test_get_border_signatures():
    tile = np.array([['#', '.', '#'], ['#', '.', '#'], ['#', '.', '.']])
    assert get_border_signatures(tile) == (3, 5, 7, 4)


def load_tiles(filename):
    size = None
    tiles = {}
    render_tiles = {}
    with open(filename, 'r') as f:
        while (header := f.readline()):
            tile_id = int(re.findall(r'^Tile ([0-9]+):$', header.strip())[0])
            tile = []
            while (line := f.readline().strip()):
                tile.append([c for c in line])
            tile = np.array(tile)
            if size is None:
                size = tile.shape[0]
            borders = get_border_signatures(tile)
            tiles[tile_id] = (tile_id, borders)
            render_tiles[tile_id] = tile[1:-1, 1:-1]
    return tiles, size, render_tiles


def find_matching_borders(b0, tiles, length):
    b0p = invert_signature(b0, length)
    for t in tiles:
        for i, b in enumerate(t[1]):
            if b == b0p:
                yield t[0], i, False
            if b == b0:
                yield t[0], i, True


def rotated(tile, n):
    tile_id, borders = tile
    return tile_id, borders[-n:] + borders[:-n]


def flipped(tile, length):
    tile_id, borders = tile
    borders = borders[0], borders[3], borders[2], borders[1]
    return tile_id, [invert_signature(b, length) for b in borders]


def flip_rotate_render(tile, flip, rotate):
    if flip:
        tile = tile[-1::-1,:]
    return np.rot90(tile, rotate)


def test_flip_rotate_render():
    map1 = np.array([['#', '#'], ['.', '.']])
    map2 = np.array([['#', '.'], ['#', '.']])
    map3 = np.array([['.', '.'], ['#', '#']])
    assert np.all(flip_rotate_render(map1, False, 1) == map2)
    assert np.all(flip_rotate_render(map2, True, 0) == map2)
    assert np.all(flip_rotate_render(map1, True, 0) == map3)
    assert np.all(flip_rotate_render(map1, False, 2) == map3)


def build_map(filename):
    tiles, size, render = load_tiles(filename)
    grid = defaultdict(lambda: [None, None, None, None])
    first = list(tiles.keys())[0]
    process = [first]
    top_left = None
    try:
        while tile := process.pop():
            other_tiles = [tiles[k] for k in tiles.keys() if k != tile]
            for border in range(4):
                if grid[tile][border] is None:
                    need_direction = (border + 2) % 4
                    for matched_tile, matched_border, flip in find_matching_borders(tiles[tile][1][border], other_tiles, size):
                        if flip:
                            tiles[matched_tile] = flipped(tiles[matched_tile], size)
                            matched_border = (matched_border + 2 * (matched_border % 2)) % 4
                        turns = 0
                        if matched_border != need_direction:
                            turns = need_direction - matched_border
                            tiles[matched_tile] = rotated(tiles[matched_tile], turns)
                        process.append(matched_tile)
                        render[matched_tile] = flip_rotate_render(render[matched_tile], flip, turns)
                        grid[tile][border] = matched_tile
                        grid[matched_tile][need_direction] = tile
                        break
            if grid[tile][2] is None and grid[tile][1] is None:
                top_left = tile
    except IndexError:
        pass
    combined_grid = build_grid(grid, top_left)
    rendered_grid = render_grid(combined_grid, render)
    return combined_grid, rendered_grid


def build_grid(grid, top_left):
    row = top_left
    res = []
    while row is not None:
        res_row = []
        col = row
        while col is not None:
            res_row.append(col)
            col = grid[col][0]
        row = grid[row][3]
        res.append(res_row)
    return np.array(res)


def render_grid(grid, tiles):
    size_tile = list(tiles.values())[0].shape[0]
    size = grid.shape[0] * size_tile
    rendered = np.empty((size, size), dtype=np.str)
    for i, row in enumerate(grid):
        for j, id in enumerate(row):
            rendered[i*size_tile:(i+1)*size_tile, j*size_tile:(j+1)*size_tile] = tiles[id]
    return rendered


def test_render_grid():
    grid = np.array([[1,2],[3,4]])
    tiles = {
        1: np.array([['A','B'],['a','b']]),
        2: np.array([['B','A'],['b','a']]),
        3: np.array([['C','D'],['c','d']]),
        4: np.array([['D','C'],['d','c']])
    }
    rendered = render_grid(grid, tiles)
    assert np.all(rendered == np.array([['A','B','B','A'],['a','b','b','a'],['C','D','D','C'],['c','d','d','c']]))


def test_build_map():
    map, render = build_map('example.dat')
    assert np.prod(np.array([map[0,0], map[0,-1], map[-1,0], map[-1,-1]],dtype=np.float64)) == 20899048083289

    example_result = np.array([[1951, 2311, 3079],[2729, 1427, 2473],[2971, 1489, 1171]])
    rot = 0
    flip = False
    for i in range(8):
        if i == 4:
            map = flip_rotate_render(map, True, 0)
            flip = True
        if np.all(example_result == map):
            break
        map = flip_rotate_render(map, False, 1)
        rot += 1

    with open('example_map_flipped.dat', 'r') as f:
        example_map = np.array([[c for c in s[:-1]] for s in f])
    render = flip_rotate_render(render, flip, rot)
    assert np.all(render == example_map)

def find_pattern(map, pattern):
    height, width = pattern.shape
    mask = pattern != '#'
    count = 0
    for y in range(0, map.shape[0] - height):
        for x in range(0, map.shape[1] - width):
            if np.all(np.logical_or(map[y:y+height,x:x+width] == pattern, mask)):
                count += 1
    return count


def test_find_pattern():
    with open('monster.dat', 'r') as f:
        monster = np.array([[c for c in s[:-1]] for s in f])
    with open('example_map.dat', 'r') as f:
        map = np.array([[c for c in s[:-1]] for s in f])
    assert find_pattern(map, monster) == 2


def find_seamonsters(map):
    with open('monster.dat', 'r') as f:
        monster = np.array([[c for c in s[:-1]] for s in f])
    for _ in range(4):
        count = find_pattern(map, monster)
        if count > 0:
            return count
        map = flip_rotate_render(map, False, 1)
    map = flip_rotate_render(map, True, 0)
    for _ in range(4):
        count = find_pattern(map, monster)
        if count > 0:
            return count
        map = flip_rotate_render(map, False, 1)


def test_find_seamonsters():
    with open('example_map_flipped.dat', 'r') as f:
        map = np.array([[c for c in s[:-1]] for s in f])
    assert find_seamonsters(map) == 2


def calculate_roughness(map):
    num_monsters = find_seamonsters(map)
    count_monster_pixels = 0
    with open('monster.dat', 'r') as f:
        for row in f:
            for c in row:
                count_monster_pixels += 1 if c == '#' else 0

    count_pixels = 0
    for row in map:
        for c in row:
            count_pixels += 1 if c == '#' else 0

    return count_pixels - num_monsters * count_monster_pixels


def test_calculate_roughness():
    with open('example_map_flipped.dat', 'r') as f:
        map = np.array([[c for c in s[:-1]] for s in f])
    assert calculate_roughness(map) == 273


map, render = build_map('input.dat')
print('\n'.join(''.join(row) for row in render))
print(int(np.prod(np.array([map[0,0], map[0,-1], map[-1,0], map[-1,-1]],dtype=np.float64))))
print(calculate_roughness(render))
