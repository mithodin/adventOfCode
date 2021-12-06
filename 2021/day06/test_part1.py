import numpy as np


class Solver:
    @staticmethod
    def solve(input_file):
        with open(input_file, "r") as puzzle_input:
            fishes = [int(f) for f in puzzle_input.readline().split(",")]
        fish = Solver.list_of_fishes_to_fish_array(fishes)
        for _ in range(80):
            fish = Solver.next_generation(fish)
        return fish.sum()

    @staticmethod
    def next_generation(fish):
        fish = np.roll(fish, -1)
        fish[6] += fish[8]
        return fish

    @staticmethod
    def list_of_fishes_to_fish_array(fishes):
        fish = np.zeros(9, dtype=np.int64)
        for f in fishes:
            fish[f] += 1
        return fish


def main():
    solution = Solver.solve("input.txt")
    print(solution)


if __name__ == "__main__":
    main()


def test_iterate_fish():
    fish = np.zeros(9, dtype=np.int64)
    fish[0] = 1

    fish = Solver.next_generation(fish)
    assert np.all(fish == [0, 0, 0, 0, 0, 0, 1, 0, 1])


def test_list_of_fishes_to_fish_array():
    fishes = [0, 1, 1, 2, 5, 6, 6, 6, 8, 8, 8, 8]
    fish = Solver.list_of_fishes_to_fish_array(fishes)

    assert np.all(fish == [1, 2, 1, 0, 0, 1, 3, 0, 4])


def test_solution():
    solution = Solver.solve("test_input.txt")

    assert solution == 5934
