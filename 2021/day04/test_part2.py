import numpy as np
import test_part1


class Solver(test_part1.Solver):
    @staticmethod
    def solve(input_file):
        numbers, boards = Solver.parse_input(input_file)
        return Solver.play_bingo(boards, numbers)

    @staticmethod
    def play_bingo(boards, numbers):
        for chosen_number in numbers:
            boards = Solver.bingo_round(boards, chosen_number)
            winner = Solver.get_winning_board(boards)
            if winner is not None:
                boards = Solver.get_remaining_boards(boards)
                if len(boards) == 0:
                    score = Solver.board_score(winner)
                    return score * chosen_number

    @staticmethod
    def get_remaining_boards(boards):
        return [board for board in boards if not Solver.is_board_winner(board)]


def main():
    solution = Solver.solve("input.txt")
    print(solution)


if __name__ == "__main__":
    main()


def test_get_remaining_boards():
    boards = [np.array([[1, 1], [1, 1]])]
    remaining = Solver.get_remaining_boards(boards)
    assert len(remaining) == 1

    boards = [np.array([[1, 1], [1, 1]]), np.array([[1, 2], [3, 4]])]
    remaining = Solver.get_remaining_boards(boards)
    assert len(remaining) == 2

    boards = [np.array([[-1, -1], [1, 1]]), np.array([[1, 2], [3, 4]])]
    remaining = Solver.get_remaining_boards(boards)
    assert len(remaining) == 1


def test_play_until_last_winner():
    boards = [np.array([[1, 1], [1, 1]]), np.array([[1, 2], [3, 4]])]
    numbers = [1, 2]

    assert Solver.play_bingo(boards, numbers) == 14


def test_solution():
    solution = Solver.solve("test_input.txt")
    assert solution == 1924
