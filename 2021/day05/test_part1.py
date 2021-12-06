import re

import numpy as np


class Solver:
    line_parse_expression = re.compile(r'([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')

    @staticmethod
    def solve(input_file):
        pass

    @staticmethod
    def parse_line(line_raw):
        try:
            x0, y0, x1, y1 = Solver.line_parse_expression.match(line_raw).groups()
        except TypeError:
            return None, None
        return (int(x0), int(y0)), (int(x1), int(y1))

    @staticmethod
    def get_lines(lines_raw):
        lines = [Solver.parse_line(line) for line in lines_raw]
        return [line for line in lines if line[0][1] == line[1][1] or line[0][0] == line[1][0]]

    @staticmethod
    def get_line_values(line):
        def add_vec(v0, v1):
            return v0[0] + v1[0], v0[1] + v1[1]

        dx = line[1][0] - line[0][0]
        dy = line[1][1] - line[0][1]
        p0 = line[0]
        step = (dx/abs(dx) if dx != 0 else 0, dy/abs(dy) if dy != 0 else 0)
        steps = abs(dx) + abs(dy) + 1
        values = np.zeros(steps, dtype=np.object)
        for i in range(steps):
            values[i] = p0
            p0 = add_vec(p0, step)
        return values

    @staticmethod
    def plot_lines(lines):
        return np.zeros((1, 1))


def main():
    solution = Solver.solve("input.txt")
    print(solution)


if __name__ == "__main__":
    main()


def test_parse_line():
    start, end = Solver.parse_line("0,1 -> 0,3")
    assert start == (0, 1)
    assert end == (0, 3)


def test_get_only_horizontal_lines():
    lines = Solver.get_lines(["1,0 -> 3,0", "0,0 -> 1,1"])
    assert len(lines) == 1
    start, end = lines[0]
    assert start == (1, 0)
    assert end == (3, 0)


def test_get_only_vertical_lines():
    lines = Solver.get_lines(["0,1 -> 0,3", "0,0 -> 1,1"])
    assert len(lines) == 1
    start, end = lines[0]
    assert start == (0, 1)
    assert end == (0, 3)


def test_get_line_values():
    line = ((0, 0), (0, 3))
    values = Solver.get_line_values(line)
    assert len(values) == 4

    assert values[0] == (0, 0)
    assert values[1] == (0, 1)
    assert values[2] == (0, 2)
    assert values[3] == (0, 3)


def test_plot_lines():
    lines = [((0, 0), (0, 3)), ((0, 5), (5, 5))]
    plot = Solver.plot_lines(lines)
    assert plot.shape == (6, 6)
