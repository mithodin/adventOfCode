#!/usr/bin/env python3

class Circle:
    def __init__(self, items):
        self.__items__ = [x for x in items]

    def __getitem__(self, item):
        size = len(self.__items__)
        if isinstance(item, slice):
            start = (item.start if item.start is not None else 0) % size
            end = item.stop if item.stop is not None else size
            if end < start:
                end += size
            e = end - size
            if e > 0:
                return Circle(self.__items__[start:] + self.__items__[:e])
            else:
                return Circle(self.__items__[start:end])
        return self.__items__[item % size]

    def __str__(self):
        return str(self.__items__)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Circle(self.__items__ + [x for x in other])

    def __iter__(self):
        return self.__items__.__iter__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            m0 = min(self.__items__)
            m1 = min(other)
            if m0 == m1:
                im0 = self.__items__.index(m0)
                im1 = other.index(m0)
                return list(self[im0+1:im0]) == list(other[im1+1:im1])
            return False
        return False

    def index(self, num):
        return self.__items__.index(num)


def play_game(initial, turns):
    max_val = max(initial)
    circle = Circle(initial)
    current = 0
    for _ in range(turns):
        yield(circle)
        taken = circle[current+1:current+4]
        subcircle = circle[current+4:current+1]
        label = circle[current] - 1
        if label == 0:
            label = max_val
        destination = None
        while destination is None:
            try:
                destination = subcircle.index(label)
            except ValueError:
                label = (label - 1) % max_val
                if label == 0:
                    label = max_val
        circle = subcircle[:destination+1] + taken + subcircle[destination+1:]
    yield(circle)


def test_play_game():
    res = [t for t in play_game([3,8,9,1,2,5,4,6,7], 10)]
    assert res[1] == Circle([3,2,8,9,1,5,4,6,7])
    assert res[2] == Circle([3,2,5,4,6,7,8,9,1])
    assert res[10] == Circle([5,8,3,7,4,1,9,2,6])


res = [t for t in play_game([9, 4, 2, 3, 8, 7, 6, 1, 5], 100)]
print(res[-1])