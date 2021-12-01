#!/usr/bin/env python3


def signature(deck):
    return int('1' + ''.join('{:02d}'.format(x) for x in deck))


def play_game(deck1, deck2):
    history = set()
    while len(deck1) > 0 and len(deck2) > 0:
        s1 = signature(deck1)
        s2 = signature(deck2)
        if (s1, s2) in history:
            return deck1, []
        history.add((s1, s2))
        c1 = deck1.pop(0)
        c2 = deck2.pop(0)
        if len(deck1) < c1 or len(deck2) < c2:
            if c1 > c2:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
        else:
            p1, p2 = play_game([x for x in deck1[:c1]], [x for x in deck2[:c2]])
            if len(p2) == 0:
                deck1.append(c1)
                deck1.append(c2)
            else:
                deck2.append(c2)
                deck2.append(c1)
    return deck1, deck2


def test_play_game():
    p1, p2 = play_game([3],[1])
    assert p1 == [3,1]
    assert p2 == []

    p1, p2 = play_game([43,19],[2,29,14])
    assert p1 == [43,19]
    assert p2 == []

    p1, p2 = play_game([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])
    assert p1 == []
    assert p2 == [7, 5, 6, 2, 4, 1, 10, 8, 9, 3]


def score(player1, player2):
    s1 = sum((len(player1) - i)*x for i,x in enumerate(player1))
    s2 = sum((len(player2) - i)*x for i,x in enumerate(player2))
    return s1, s2


def test_score():
    p1, p2 = play_game([9, 2, 6, 3, 1], [5, 8, 4, 7, 10])
    assert score(p1, p2) == (0, 291)


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
    p1, p2 = play_game(p1, p2)
    print(score(p1, p2))


load_game('input.dat')
