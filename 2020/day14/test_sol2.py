#!/usr/bin/env python3
import re
from itertools import combinations


def make_masks(mask):
    or_mask = int(''.join(['1' if s == '1' else '0' for s in mask]), 2)
    and_mask = int(''.join(['0' if s == 'X' else '1' for s in mask]), 2)
    floating_bits = [len(mask)-1-i for i, s in enumerate(mask) if s == 'X']

    def gen_addresses(address):
        address |= or_mask
        address &= and_mask
        for length in range(len(floating_bits)+1):
            for ones in combinations(floating_bits, length):
                yield address | sum(2**bit for bit in ones)

    return gen_addresses


decode_instruction = re.compile(r'^(m[askem]+)(\[([0-9]+)\])? = ([X0-9]+)$')
def execute_program(instructions):
    mem = {}
    mask = lambda: None
    for instruction in instructions:
        ins, _, arg1, arg0 = decode_instruction.findall(instruction)[0]
        if ins == 'mask':
            mask = make_masks(arg0)
        elif ins == 'mem':
            value = int(arg0)
            address = int(arg1)
            for addr in mask(address):
                mem[addr] = value
    return mem


def test_execute_program():
    with open('example2.dat', 'r') as f:
        instructions = [s.strip() for s in f]
    mem = execute_program(instructions)
    assert sum(mem.values()) == 208


with open('input.dat', 'r') as f:
    instructions = [s.strip() for s in f]
print(sum(execute_program(instructions).values()))
