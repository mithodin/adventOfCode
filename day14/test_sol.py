#!/usr/bin/env python3
import re


def make_masks(mask):
    and_mask = int(''.join(['0' if s == '0' else '1' for s in mask]), 2)
    or_mask = int(''.join(['1' if s == '1' else '0' for s in mask]), 2)
    return and_mask, or_mask


decode_instruction = re.compile(r'^(m[askem]+)(\[([0-9]+)\])? = ([X0-9]+)$')
def execute_program(instructions):
    mem = {}
    and_mask, or_mask = 0, 0
    for instruction in instructions:
        ins, _, arg1, arg0 = decode_instruction.findall(instruction)[0]
        if ins == 'mask':
            and_mask, or_mask = make_masks(arg0)
        elif ins == 'mem':
            value = int(arg0) & and_mask | or_mask
            address = int(arg1)
            mem[address] = value
    return mem


def test_execute_program():
    with open('example.dat', 'r') as f:
        instructions = [s.strip() for s in f]
    mem = execute_program(instructions)
    assert mem[7] == 101
    assert mem[8] == 64
    assert sum(mem.values()) == 165


with open('input.dat', 'r') as f:
    instructions = [s.strip() for s in f]
print(sum(execute_program(instructions).values()))
