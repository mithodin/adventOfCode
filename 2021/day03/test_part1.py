import numpy as np


def test_parse_sideways():
    class MockFile:
        def readlines(self):
            yield "1000\n"
            yield "0100\n"
            yield "0010\n"

    result = parse_sideways(MockFile())

    assert result.shape == (4, 3)
    assert np.all(result == np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]]))


def test_most_common_bit():
    data = np.array([1, 0, 0, 1, 0, 0, 1])
    assert most_common_bit(data) == 0

    data = np.array([1, 1, 0, 1, 0, 0, 1])
    assert most_common_bit(data) == 1

    data = np.array([1, 1, 0, 0])
    assert most_common_bit(data) == 1


def test_get_gamma_epsilon():
    data = np.array([[1, 1, 0], [0, 1, 0]])
    gamma, epsilon = get_gamma_epsilon(data)
    assert gamma == 2
    assert epsilon == 1

    data = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    gamma, epsilon = get_gamma_epsilon(data)
    assert gamma == 4
    assert epsilon == 3


def test_parse_gamma_epsilon():
    class MockFile:
        def readlines(self):
            for line in ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]:
                yield line + "\n"

    gamma, epsilon = parse_gamma_epsilon(MockFile())
    assert gamma == 22
    assert epsilon == 9


def parse_sideways(file_handle):
    return iterate_sideways(file_handle.readlines())


def iterate_sideways(lines):
    parsed = []
    for line in lines:
        parsed.append([int(c) for c in line.strip()])
    return np.array(parsed).transpose()


def most_common_bit(array):
    return 1 if array.sum() >= array.shape[0] / 2 else 0


def get_gamma_epsilon(data):
    gamma_as_str = "".join([str(most_common_bit(line)) for line in data])
    epsilon_as_str = "".join(["1" if c == "0" else "0" for c in gamma_as_str])
    return int(gamma_as_str, 2), int(epsilon_as_str, 2)


def parse_gamma_epsilon(file_handle):
    lines = parse_sideways(file_handle)
    return get_gamma_epsilon(lines)


def main():
    with open("input.txt") as input_file:
        gamma, epsilon = parse_gamma_epsilon(input_file)
        print(gamma * epsilon)


if __name__ == "__main__":
    main()
