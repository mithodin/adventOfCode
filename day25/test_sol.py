#!/usr/bin/env python3
from math import ceil, sqrt
from mod import Mod
from numpy import genfromtxt

def find_value_sorted(arr, val, key=lambda x: x):
    l = len(arr)
    if l == 0:
        return
    m = l//2
    vm = key(arr[m])
    if vm > val:
        return find_value_sorted(arr[:m], val, key)
    if vm < val:
        r = find_value_sorted(arr[m+1:], val, key)
        return r + m + 1 if r is not None else None
    return m


def test_find_value_sorted():
    s = [1,2,3,4,5,6,7,8,9,10]
    assert find_value_sorted(s, 7) == 6
    assert find_value_sorted(s, 11) is None


modulus = 20201227
base = 7
def find_pq(b, n, mod=modulus, a=base):
    print(b, n, mod, a)
    a = Mod(a,mod)
    b = Mod(b,mod)
    max_p = ceil(mod/n)
    max_q = n
    n = Mod(n,mod)
    vals_p = sorted([(p, a**(n*p)) for p in range(1, max_p+1)], key=lambda x: x[1])
    for q in range(max_q+1):
        q = Mod(q,mod)
        val_q = b*a**q
        ip = find_value_sorted(vals_p, val_q, lambda x: x[1])
        if ip is not None:
            return vals_p[ip][0], q


def find_exponent(b, mod=modulus, a=base):
    n = round(sqrt(mod))
    p, q = find_pq(b, n, mod, a)
    return n * p - q


def test_find_exponent():
    assert find_exponent(7, mod=13, a=7) == 1
    assert find_exponent(7**2, mod=13, a=7) == 2
    assert find_exponent(8, mod=17, a=8) == 1
    assert find_exponent(8**13, mod=17, a=8) == 13
    assert find_exponent(5764801) == 8
    assert find_exponent(17807724) == 11


def find_encryption_key(p1, p2):
    return (p2 ** find_exponent(p1))


def test_find_encryption_key():
    assert find_encryption_key(5764801, 17807724) == 14897079
    assert find_encryption_key(17807724, 5764801) == 14897079


pubkeys = genfromtxt('input.dat', dtype='int64')
print(find_encryption_key(*pubkeys))