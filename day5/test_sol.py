#!/usr/bin/env python3

def parse_seat_number(seat):
    seat = "".join(['1' if c == 'B' or c == 'R' else '0' for c in seat])
    seat_id = int(seat, 2)
    return seat_id // 8, seat_id % 8, seat_id


def test_parse_seat_number():
    assert parse_seat_number('BFFFBBFRRR') == (70, 7, 567)
    assert parse_seat_number('FFFBBBFRRR') == (14, 7, 119)
    assert parse_seat_number('BBFFBBFRLL') == (102, 4, 820)
    assert parse_seat_number('FBFBBFFRLR') == (44, 5, 357)


def find_missing(ids):
    ids = sorted(ids)
    prev = ids[0]
    for id in ids[1:]:
        if id - prev != 1:
            return id-1
        prev = id



with open('input.dat','r') as f:
    ids = [parse_seat_number(l.strip())[2] for l in f]
print(max(ids))

print(find_missing(ids))