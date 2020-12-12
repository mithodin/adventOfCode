#!/usr/bin/env python3
import cmath
import re

handlers = {
    'N': lambda sp, wp, arg: (sp, wp + arg * 1j),
    'S': lambda sp, wp, arg: (sp, wp - arg * 1j),
    'E': lambda sp, wp, arg: (sp, wp + arg),
    'W': lambda sp, wp, arg: (sp, wp - arg),
    'L': lambda sp, wp, arg: (sp, wp * cmath.exp(1j * arg / 180 * cmath.pi)),
    'R': lambda sp, wp, arg: (sp, wp * cmath.exp(-1j * arg / 180 * cmath.pi)),
    'F': lambda sp, wp, arg: (sp + arg * wp, wp),
}
parse_instruction = re.compile(r'^([NSEWLRF])([0-9]+)$')
def drive_ship(instructions):
    sp = 0
    wp = 10 + 1j
    for instruction in instructions:
        action, argument = parse_instruction.match(instruction).groups()
        sp, wp = handlers[action](sp, wp, int(argument))
    return round(sp.real)+round(sp.imag)*1j, round(wp.real)+round(wp.imag)*1j


def test_drive_ship():
    instructions = ['F10', 'N3', 'F7', 'R90', 'F11']
    assert drive_ship(instructions) == (214 - 72j, 4 - 10j)
    assert drive_ship(instructions[:-1]) == (170 + 38j, 4 - 10j)
    assert drive_ship(instructions[:-2]) == (170 + 38j, 10 + 4j)


with open('input.dat','r') as f:
    instructions = [x.strip() for x in f]
(sp, wp) = drive_ship(instructions)
print(round(abs(sp.imag)+abs(sp.real)))