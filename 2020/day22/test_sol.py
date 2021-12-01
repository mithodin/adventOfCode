#!/usr/bin/env python3


def play_game(deck1, deck2):
    while len(deck1) > 0 and len(deck2) > 0:
        yield [x for x in deck1], [x for x in deck2]
        c1 = deck1.pop(0)
        c2 = deck2.pop(0)
        if c1 > c2:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)
    yield [x for x in deck1], [x for x in deck2]


def test_play_game():
    g = [t for t in play_game([3],[1])]
    assert g[0][0] == [3]
    assert g[0][1] == [1]
    assert g[1][0] == [3,1]
    assert g[1][1] == []

    g = [t for t in play_game([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])]
    assert g[-1][0] == []
    assert g[-1][1] == [3, 2, 10, 6, 8, 5, 9, 4, 7, 1]


def score(player1, player2):
    s1 = sum((len(player1) - i)*x for i,x in enumerate(player1))
    s2 = sum((len(player2) - i)*x for i,x in enumerate(player2))
    return s1, s2


def test_score():
    g = [t for t in play_game([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])]
    s1, s2 = score(*g[-1])
    assert s1 == 0
    assert s2 == 306


def load_game(filename):
    with open(filename, 'r') as f:
        f.readline()
        p1 = []
        while (line := f.readline().strip()) != '':
            p1.append(int(line))
        f.readline()
        p2 = []
        while (line := f.readline().strip()) != '':
            p2.append(int(line))
    g = [t for t in play_game(p1, p2)]
    print(score(*g[-1]))


load_game('input.dat')
