#!/usr/bin/env python3
from lark import Lark

class Parser:
    def __init__(self, grammarfile):
        with open(grammarfile, 'r') as f:
            grammar = ''.join(f.readlines())
            self.parser = Lark(grammar, start='expr')
            self.tree = None

    def parse(self, expression):
        self.tree = self.parser.parse(expression)
        return self

    def evaluate(self):
        def add(tree):
            return e(tree.children[0]) + e(tree.children[1])
        def mul(tree):
            return e(tree.children[0]) * e(tree.children[1])
        def number(tree):
            return int(tree.children[0][0])
        mapping = {
            'add': add,
            'mul': mul,
            'number': number
        }
        def e(tree):
            return mapping[tree.data](tree)

        if self.tree is not None:
            return e(self.tree)


def test_parse():
    parser = Parser('grammar.lark')
    assert parser.parse('1 + 1').evaluate() == 2
    assert parser.parse('1 + 2 * 3 + 4 * 5 + 6').evaluate() == 71
    assert parser.parse('1 + (2 * 3) + (4 * (5 + 6))').evaluate() == 51


def test_parse2():
    parser = Parser('grammar2.lark')
    assert parser.parse('1 + 1').evaluate() == 2
    assert parser.parse('1 + 2 * 3 + 4 * 5 + 6').evaluate() == 231
    assert parser.parse('1 + (2 * 3) + (4 * (5 + 6))').evaluate() == 51
    assert parser.parse('2 * 3 + (4 * 5)').evaluate() == 46
    assert parser.parse('5 + (8 * 3 + 9 + 3 * 4 * 3)').evaluate() == 1445
    assert parser.parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))').evaluate() == 669060
    assert parser.parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2').evaluate() == 23340


with open('input.dat', 'r') as f:
    parser1 = Parser('grammar.lark')
    parser2 = Parser('grammar2.lark')
    sum1 = 0
    sum2 = 0
    for line in f:
        sum1 += parser1.parse(line.strip()).evaluate()
        sum2 += parser2.parse(line.strip()).evaluate()
    print(sum1)
    print(sum2)

