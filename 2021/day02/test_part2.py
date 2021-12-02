from typing import Callable
from test_part1 import parse_raw


def test_parse_down():
    pos_now = (0, 0, 0)
    transform = parse_command("down 1")
    assert transform(*pos_now) == (0, 0, 1)

    transform = parse_command("down 4")
    assert transform(*pos_now) == (0, 0, 4)


def test_parse_up():
    pos_now = (0, 0, 0)
    transform = parse_command("up 1")
    assert transform(*pos_now) == (0, 0, -1)

    transform = parse_command("up 5")
    assert transform(*pos_now) == (0, 0, -5)


def test_parse_forward():
    pos_now = (0, 0, 0)
    transform = parse_command("forward 1")
    assert transform(*pos_now) == (1, 0, 0)

    pos_now = (0, 0, 1)
    transform = parse_command("forward 1")
    assert transform(*pos_now) == (1, 1, 1)

    pos_now = (0, 0, 1)
    transform = parse_command("forward 2")
    assert transform(*pos_now) == (2, 2, 1)


def test_final_location():
    assert parse_directions(
        map(lambda s: s.strip(),
            """forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2""".split("\n"))
    ) == (15, 60)


def parse_command(command) -> Callable:
    commands = {
        "down": lambda x, y, aim, delta: (x, y, aim + delta),
        "up": lambda x, y, aim, delta: (x, y, aim - delta),
        "forward": lambda x, y, aim, delta: (x + delta, y + aim * delta, aim)
    }
    amount, command = parse_raw(command)
    try:
        action = commands[command]
    except KeyError:
        action = lambda x, y, aim, _: (x, y, aim)
    return lambda x, y, aim: action(x, y, aim, int(amount))


def parse_directions(commands):
    pos = (0, 0, 0)
    for command in commands:
        pos = parse_command(command)(*pos)
    return pos[0], pos[1]


def main():
    with open("input.txt") as my_input:
        pos = parse_directions(my_input.readlines())
    print(pos[0] * pos[1])


if __name__ == "__main__":
    main()
