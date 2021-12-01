#!/usr/bin/env python3
import itertools


def game(starting_numbers):
    mem = {n: i+1 for i, n in enumerate(starting_numbers)}
    for n in starting_numbers:
        yield n
    k = len(starting_numbers)
    prev = starting_numbers[-1]
    while True:
        try:
            n = k - mem[prev]
        except KeyError:
            n = 0
        yield n
        mem[prev] = k
        prev = n
        k += 1


def test_game():
    assert list(itertools.islice(game([0, 3, 6]), 10)) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]


def nth_game_turn(starting_numbers, n):
    return list(itertools.islice(game(starting_numbers), n-1, n))[0]


def test_nth_game_turn():
    assert nth_game_turn([0, 3, 6], 2020) == 436
    assert nth_game_turn([1, 3, 2], 2020) == 1
    assert nth_game_turn([2, 1, 3], 2020) == 10
    assert nth_game_turn([1, 2, 3], 2020) == 27
    assert nth_game_turn([2, 3, 1], 2020) == 78
    assert nth_game_turn([2, 3, 1], 2020) == 78
    assert nth_game_turn([3, 2, 1], 2020) == 438
    assert nth_game_turn([2, 3, 1], 2020) == 78
    assert nth_game_turn([3, 1, 2], 2020) == 1836
    assert nth_game_turn([0, 3, 6], 30000000) == 175594
    assert nth_game_turn([1, 3, 2], 30000000) == 2578
    assert nth_game_turn([2, 1, 3], 30000000) == 3544142
    assert nth_game_turn([1, 2, 3], 30000000) == 261214
    assert nth_game_turn([2, 3, 1], 30000000) == 6895259
    assert nth_game_turn([3, 2, 1], 30000000) == 18
    assert nth_game_turn([3, 1, 2], 30000000) == 362


print(nth_game_turn([12,1,16,3,11,0], 2020))
print(nth_game_turn([12,1,16,3,11,0], 30000000))
