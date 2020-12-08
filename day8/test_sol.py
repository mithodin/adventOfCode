#!/usr/bin/env python3
import re

instr = {
    'acc': lambda inp, acc, arg: (inp + 1, acc + arg),
    'nop': lambda inp, acc, arg: (inp + 1, acc),
    'jmp': lambda inp, acc, arg: (inp + arg, acc)
}
format = re.compile(r'(acc|nop|jmp) ([+\-][0-9]+)')
def machine(instructions):
    inp = 0
    acc = 0
    try:
        while (instruction := instructions[inp]) is not None:
            instructions[inp] = None
            (ins, arg) = format.findall(instruction)[0]
            (inp, acc) = instr[ins](inp, acc, int(arg))
    except IndexError:
        pass
    return inp, acc


def flipped(instruction):
    (ins, arg) = format.findall(instruction)[0]
    ins = {'nop': 'jmp', 'jmp': 'nop'}[ins]
    return "{} {}".format(ins, arg)


def fix_instructions(instructions):
    for i in range(len(instructions)):
        copy_ins = [x for x in instructions]
        try:
            copy_ins[i] = flipped(copy_ins[i])
        except KeyError:
            continue
        (inp, acc) = machine(copy_ins)
        if inp == len(copy_ins):
            return acc


def test_machine():
    assert machine(['acc +1', 'jmp -1']) == (0, 1)
    assert machine(['acc +1']) == (1, 1)
    with open('example.dat', 'r') as f:
        instructions = [x.strip() for x in f]
    assert machine(instructions) == (1, 5)
    with open('example_mod.dat', 'r') as f:
        instructions = [x.strip() for x in f]
    assert machine(instructions) == (len(instructions), 8)


def test_fix_instructions():
    with open('example.dat', 'r') as f:
        instructions = [x.strip() for x in f]
        assert fix_instructions(instructions) == 8


with open('input.dat', 'r') as f:
    instructions = [x.strip() for x in f]
print(machine([x for x in instructions]))
print(fix_instructions(instructions))


