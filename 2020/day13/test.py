def day13_part2(data):
    bus_ids = [int(num) if num != "x" else -1 for num in data[1].split(",")]

    time = bus_ids[0]
    incrementer = bus_ids[0]

    while True:
        for index in range(1, len(bus_ids)):
            if bus_ids[index] == -1:
                continue

            # We found a new multiple of all the prior found busses
            # plus this, so we can multiply by this and increment even faster
            if (time + index) % bus_ids[index] == 0:
                incrementer *= bus_ids[index]
                bus_ids[index] = -1

        # We've accounted for all busses, we're done!
        if all(bus_id == -1 for bus_id in bus_ids[1:]):
            break

        time += incrementer

    return time

print(day13_part2([[],"2,3,5,7"]))