#!/usr/bin/env python3

def load_preprocess_data(filename):
    with open(filename, 'r') as f:
        groups = [g.strip().split('\n') for g in ''.join(f.readlines()).split('\n\n')]
    return groups


def common_answers(group):
    common = set([s for s in group[0]])
    for person in group[1:]:
        answers = set([s for s in person])
        common = common.intersection(answers)
    return len(common)


def test_unique_answers():
    groups = load_preprocess_data('example.dat')
    assert [common_answers(g) for g in groups] == [3, 3, 0, 1, 1, 1]


print(sum([common_answers(g) for g in load_preprocess_data('input.dat')]))
