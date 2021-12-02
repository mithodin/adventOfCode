import numpy as np


def test_returns_same_shape():
    data = np.array([199, 200])
    result = depth_delta(data)
    assert data.shape == result.shape


def test_returns_zero_for_first_element():
    data = np.array([199, 200])
    assert depth_delta(data)[0] == 0


def test_returns_positive_value_for_increase():
    data = np.array([199, 200])
    assert depth_delta(data)[1] > 0


def test_returns_negative_value_for_decrease():
    data = np.array([200, 199])
    assert depth_delta(data)[1] < 0


def test_list_of_depths():
    data = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    result = depth_delta(data)
    assert result[0] == 0
    assert np.all(result[[1, 2, 3, 5, 6, 7, 9]] > 0)
    assert np.all(result[[4, 8]] < 0)


def depth_delta(array):
    return np.concatenate(([0], array[1:] - array[:-1]))


def main():
    data = np.genfromtxt("input.txt")
    deltas = depth_delta(data)
    increases = np.count_nonzero(deltas > 0)
    print(increases)


if __name__ == "__main__":
    main()
