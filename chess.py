
from coordinates import Coordinates
from square import Square


def generate_new_board() -> list[list[Square]]:
    board_dimensions = Coordinates((8, 8))
    board: list[list[Square]] = []

    for i in range(board_dimensions.y):
        row: list[Square] = []

        for j in range(board_dimensions.x):
            coordinates = Coordinates((i, j))
            row.append(Square(coordinates))

        board.append(row)

    return board

board = generate_new_board()

def display_board(board: list[list[Square]]) -> None:
    board_dimensions = Coordinates((8, 8))

    print("\n" + "  ", end = '')

    for i in range(board_dimensions.x):
        column_number = i + 1
        print("| %s " %column_number, end = '')

    print("| ")
    print_row_break(board_dimensions.x)

    for row in board:
        print("%s " %chr(65), end='')

        for square in row:
            print("| %s " %square.symbol, end='')

        print("| ")
        print_row_break(board_dimensions.x)

    print("\n")

def print_row_break(row_length: int):
    dashes_per_column = 4
    print("-" * (row_length + 1) * dashes_per_column)

display_board(board)
