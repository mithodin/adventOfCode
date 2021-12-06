import test_part1


class Solver(test_part1.Solver):
    @staticmethod
    def solve(input_file):
        with open(input_file, "r") as puzzle_input:
            fishes = [int(f) for f in puzzle_input.readline().split(",")]
        fish = Solver.list_of_fishes_to_fish_array(fishes)
        for _ in range(256):
            fish = Solver.next_generation(fish)
        return fish.sum()


def main():
    solution = Solver.solve("input.txt")
    print(solution)


if __name__ == "__main__":
    main()
