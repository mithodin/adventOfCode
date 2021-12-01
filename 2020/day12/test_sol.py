#!/usr/bin/env python3
import math
import re

handlers = {
    'N': lambda x, y, h, arg: (x, y + arg, h),
    'S': lambda x, y, h, arg: (x, y - arg, h),
    'E': lambda x, y, h, arg: (x + arg, y, h),
    'W': lambda x, y, h, arg: (x - arg, y, h),
    'L': lambda x, y, h, arg: (x, y, h + arg / 180 * math.pi),
    'R': lambda x, y, h, arg: (x, y, h - arg / 180 * math.pi),
    'F': lambda x, y, h, arg: (x + arg * math.cos(h), y + arg * math.sin(h), h),
}
parse_instruction = re.compile(r'^([NSEWLRF])([0-9]+)$')
def drive_ship(instructions):
    x = 0
    y = 0
    h = 0
    for instruction in instructions:
        action, argument = parse_instruction.match(instruction).groups()
        x, y, h = handlers[action](x, y, h, int(argument))
    return x, y, h


def test_drive_ship():
    instructions = ['F10', 'N3', 'F7', 'R90', 'F11']
    assert drive_ship(instructions) == (17, -8, -math.pi/2)


with open('input.dat','r') as f:
    instructions = [x.strip() for x in f]
(x, y, h) = drive_ship(instructions)
print(abs(x)+abs(y))