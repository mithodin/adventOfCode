#!/usr/bin/env python3
import numpy as np

def solution1(numbers, target):
    for i in range(len(numbers)-1):
        try:
            j = np.where(numbers[i]+numbers[(i+1):] == target)[0][0]
            return numbers[i]*numbers[i+1+j]
        except IndexError:
            pass
    return None

def test1():
    numbers = np.array([1721,979,366,299,675,1456])
    assert solution1(numbers, 2020) == 514579

def solution2(numbers, target):
    for i in range(len(numbers)-2):
        for j in range(i+1,len(numbers)-1):
            try:
                k = np.where(numbers[i]+numbers[j]+numbers[(j+1):] == target)[0][0]
                return numbers[i]*numbers[j]*numbers[j+1+k]
            except IndexError:
                pass
    return None

def test2():
    numbers = np.array([1721,979,366,299,675,1456])
    assert solution2(numbers, 2020) == 241861950

numbers = np.genfromtxt('input.dat')
print(solution1(numbers, 2020))
print(solution2(numbers, 2020))
