import numpy as np


class Solver:
    @staticmethod
    def solve(input_file):
        numbers, boards = Solver.parse_input(input_file)
        return Solver.play_bingo(boards, numbers)

    @staticmethod
    def mark(board, chosen_number):
        board[board == chosen_number] = -1
        return board

    @staticmethod
    def is_board_winner(board):
        return bool(np.any(np.all(board < 0, axis=1)) or np.any(np.all(board < 0, axis=0)))

    @staticmethod
    def board_score(board):
        return np.sum(board[board >= 0])

    @staticmethod
    def bingo_round(boards, chosen_number):
        for board in boards:
            Solver.mark(board, chosen_number)
        return boards

    @staticmethod
    def get_winning_board(boards):
        for board in boards:
            if Solver.is_board_winner(board):
                return board

    @staticmethod
    def play_bingo(boards, numbers):
        for chosen_number in numbers:
            boards = Solver.bingo_round(boards, chosen_number)
            winner = Solver.get_winning_board(boards)
            if winner is not None:
                score = Solver.board_score(winner)
                return score * chosen_number

    @staticmethod
    def parse_input(file_name):
        with open(file_name, "r") as file_input:
            numbers_raw = file_input.readline().strip()
            file_input.readline()
            boards_raw = []
            board = []
            for line in file_input.readlines():
                line = line.strip()
                if len(line) == 0:
                    boards_raw.append(board)
                    board = []
                else:
                    board.append(line)
            if len(board) > 0:
                boards_raw.append(board)
        numbers = [int(num) for num in numbers_raw.split(",")]
        boards = [Solver.parse_board(board_raw) for board_raw in boards_raw]
        return numbers, boards

    @staticmethod
    def parse_board(board_raw):
        return np.array([[int(num) for num in line.split(" ") if len(num) > 0] for line in board_raw])


def main():
    solution = Solver.solve("input.txt")
    print(solution)


if __name__ == "__main__":
    main()


def test_mark_number():
    board = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    Solver.mark(board, 2)
    assert board[0, 1] == -1
    assert np.all(board[:, 2:] >= 0)


def test_is_board_winner():
    board = np.array([[-1, -2], [3, 4]])
    assert Solver.is_board_winner(board) is True

    board = np.array([[1, -2], [-3, 4]])
    assert Solver.is_board_winner(board) is False

    board = np.array([[-1, 2], [-3, 4]])
    assert Solver.is_board_winner(board) is True


def test_board_score():
    board = np.array([[-1, -2], [3, 4]])
    assert Solver.board_score(board) == 7


def test_bingo_round():
    boards = np.array([np.array([[1, 2], [3, 4]]), np.array([[5, 1], [7, 9]])])
    boards = Solver.bingo_round(boards, 1)
    assert boards[0][0, 0] == -1
    assert boards[1][0, 1] == -1

    boards = np.array([np.array([[1, 2], [3, 4]]), np.array([[5, 1], [7, 9]])])
    boards = Solver.bingo_round(boards, 10)
    for board in boards:
        assert np.all(board >= 0)


def test_play_bingo():
    boards = np.array([np.array([[1, 2], [3, 4]]), np.array([[5, 1], [7, 9]])])
    winning_score = Solver.play_bingo(boards, [1, 7, 10, 12, 2])
    assert winning_score == 14


def test_parse_input():
    numbers, boards = Solver.parse_input("test_input.txt")
    assert len(boards) == 3
    assert numbers == [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    assert np.all(boards[0] == np.array([[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]))
    assert np.all(boards[1] == np.array([[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]]))


def test_solution():
    solution = Solver.solve("test_input.txt")
    assert solution == 4512
