import re


def test_parse_forward():
    assert parse_command("forward 1") == (1, 0)
    assert parse_command("forward 5") == (5, 0)


def test_parse_down():
    assert parse_command("down 1") == (0, 1)
    assert parse_command("down 3") == (0, 3)


def test_parse_up():
    assert parse_command("up 1") == (0, -1)
    assert parse_command("up 2") == (0, -2)


def test_final_location():
    assert parse_directions([
        "down 1",
        "forward 2",
        "up 2",
        "down 3",
        "forward 1"
    ]) == (3, 2)

    assert parse_directions(
        map(lambda s: s.strip(),
            """forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2""".split("\n"))
    ) == (15, 10)


def vec_scale(vec, factor):
    return vec[0] * factor, vec[1] * factor


def vec_add(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def parse_command(command_input):
    commands = {
        "forward": (1, 0),
        "down": (0, 1),
        "up": (0, -1)
    }
    amount, command = parse_raw(command_input)
    try:
        base_vector = commands[command]
    except KeyError:
        return 0, 0
    return vec_scale(base_vector, int(amount))


def parse_raw(command_input):
    parser = re.compile(r'([a-z]+)\s([0-9]+)')
    command, amount = parser.match(command_input).groups()
    return amount, command


def parse_directions(commands):
    pos = (0, 0)
    for command in commands:
        pos = vec_add(pos, parse_command(command))
    return pos


def main():
    with open("input.txt") as my_input:
        pos = parse_directions(my_input.readlines())
    print(pos[0] * pos[1])


if __name__ == "__main__":
    main()
