import numpy as np

from test_part1 import depth_delta


def test_smoothed_length():
    data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    assert smooth(data).shape[0] == 8


def test_average_first_element():
    data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    assert smooth(data)[0] == 607


def test_smoothed_values():
    data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    assert np.all(smooth(data) == [607, 618, 618, 617, 647, 716, 769, 792])


def smooth(data):
    return data[:-2] + data[1:-1] + data[2:]


def main():
    data = np.genfromtxt("input.txt")
    smoothed = smooth(data)
    deltas = depth_delta(smoothed)
    increases = np.count_nonzero(deltas > 0)
    print(increases)


if __name__ == "__main__":
    main()
