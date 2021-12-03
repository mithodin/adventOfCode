import numpy as np
from test_part1 import iterate_sideways, most_common_bit


def test_filter_lines_by_char_at():
    lines = np.array(["100", "011", "001"])
    chosen, discarded = filter_by_char_at(lines, 0, "0")
    assert np.all(chosen == ["011", "001"])
    assert np.all(discarded == ["100"])

    chosen, discarded = filter_by_char_at(lines, 1, "0")
    assert np.all(chosen == ["100", "001"])
    assert np.all(discarded == ["011"])

    chosen, discarded = filter_by_char_at(lines, 2, "0")
    assert np.all(chosen == ["100"])
    assert np.all(discarded == ["011", "001"])


def test_filter_by_common_char_at():
    lines = np.array(["100", "011", "001", "101"])
    chosen, discarded = filter_by_common_char_at(lines, 0)
    assert np.all(chosen == ["100", "101"])


def test_filter_cascade():
    lines = np.array(["100", "011", "001", "101"])
    chosen = filter_cascade_by_common_char(lines)
    assert np.all(chosen == ["101"])

    lines = np.array(["100", "011", "001", "101"])
    chosen = filter_cascade_by_common_char(lines, invert_char)
    assert np.all(chosen == ["001"])


def test_get_oxygen_co2():
    lines = np.array(["100", "011", "001", "101"])
    oxygen, co2 = get_oxygen_co2(lines)
    assert oxygen == "101"
    assert co2 == "001"


def test_parse_oxygen_co2():
    class MockFile:
        def readlines(self):
            for line in ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]:
                yield line + "\n"

    oxygen, co2 = parse_oxygen_co2(MockFile())
    assert oxygen == 23
    assert co2 == 10


def filter_by_char_at(lines, position, desired_char):
    condition = np.vectorize(lambda string: string[position] == desired_char)
    check_result = condition(lines)
    return lines[check_result], lines[np.logical_not(check_result)]


def filter_by_common_char_at(lines, position, transform_char=lambda x: x):
    parsed = iterate_sideways(lines)
    common_char = str(most_common_bit(parsed[position]))
    return filter_by_char_at(lines, position, transform_char(common_char))


def filter_cascade_by_common_char(lines, transform_char=lambda x: x, offset=0):
    len_lines = len(lines[0])
    for i in range(offset, len_lines):
        lines, _ = filter_by_common_char_at(lines, i, transform_char)
        if len(lines) == 1:
            break
    return lines


def invert_char(c):
    return "1" if c == "0" else "0"


def get_oxygen_co2(lines):
    oxygen, co2 = filter_by_common_char_at(lines, 0)
    oxygen = filter_cascade_by_common_char(oxygen, lambda x: x, 1)
    co2 = filter_cascade_by_common_char(co2, invert_char, 1)
    return oxygen[0], co2[0]


def parse_oxygen_co2(file_handle):
    lines = np.array([line.strip() for line in file_handle.readlines()])
    oxygen, co2 = get_oxygen_co2(lines)
    return int(oxygen, 2), int(co2, 2)


def main():
    with open("input.txt") as file_input:
        oxygen, co2 = parse_oxygen_co2(file_input)
        print(oxygen*co2)


if __name__ == "__main__":
    main()
