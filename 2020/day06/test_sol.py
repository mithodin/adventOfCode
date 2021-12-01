#!/usr/bin/env python3

def load_preprocess_data(filename):
    with open(filename, 'r') as f:
        groups = [g.replace('\n', '') for g in ''.join(f.readlines()).split('\n\n')]
    return groups


def unique_answers(group):
    return len(set([x for x in group]))


def test_unique_answers():
    groups = load_preprocess_data('example.dat')
    assert [unique_answers(g) for g in groups] == [6, 3, 3, 3, 1, 1]


print(sum([unique_answers(g) for g in load_preprocess_data('input.dat')]))
