#!/usr/bin/env python3
import numpy as np

class Circle:
    __left__ = None
    __right__ = None
    __value__ = None
    __lut__ = {}

    def __init__(self, value=None, left=None, right=None, values=None):
        if left is not None:
            self.link_left(left)
        if right is not None:
            self.link_right(right)
        if value is not None:
            self.__value__ = value
            self.__lut__[value] = self
        if values is not None:
            self.__value__ = values[0]
            self.__lut__[values[0]] = self
            l = self
            for val in values[1:]:
                l = Circle(val, left=l)
            self.link_left(l)

    def link_left(self, other):
        self.__left__ = other
        if other is not None:
            other.__right__ = self

    def link_right(self, other):
        self.__right__ = other
        if other is not None:
            other.__left__ = self

    def insert(self, other_s, n):
        other_e = other_s
        for _ in range(n-1):
            other_e = other_e.__right__
        r = self.__right__
        ll = other_s.__left__
        rr = other_e.__right__
        self.link_right(other_s)
        other_e.link_right(r)
        ll.link_right(rr)

    def value(self):
        return self.__value__

    def __repr__(self):
        vals = [str(self.__value__)]
        r = self.__right__
        while r != self:
            vals.append(str(r.__value__))
            r = r.__right__
        return ', '.join(vals)

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start if item.start is not None else 0
            stop = (item.stop if item.stop is not None else 0) - start
            r = self
            vals = []
            for _ in range(start):
                r = r.__right__
            for _ in range(stop):
                vals.append(r.__value__)
                r = r.__right__
            return vals
        return self.__lut__[item]


def print_game(circle, current):
    print(circle)
    print(' '*(1+2*current)+'▲ ')


def play_game(initial, turns):
    max_val = np.max(initial)
    circle = Circle(values=initial)
    for _ in range(turns):
        #print(circle)
        taken = circle[:4]
        label = circle.value()
        while label in taken:
            label -= 1
            if label == 0:
                label = max_val
        destination = circle[label]
        destination.insert(circle.__right__,3)
        circle = circle.__right__
    #print(circle)
    return circle


def test_play_game():
    res = play_game([3,8,9,1,2,5,4,6,7], 10)
    assert res[:9] == [8,3,7,4,1,9,2,6,5]
    assert res[1][1:3] == [9,2]
    res = play_game(np.array([9, 4, 2, 3, 8, 7, 6, 1, 5]), 100)[:9]
    assert res == [4, 2, 8, 9, 7, 1, 3, 6, 5]

res = play_game([9,4,2,3,8,7,6,1,5] + [x for x in range(10,1000001)], 10000000)
a,b = res[1][1:3]
print(a*b)