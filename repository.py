
from board import Board


def display_board(board: Board) -> None:
    board_dimensions = board.shape

    print("\n" + "  ", end = '')

    for i in range(board_dimensions.x):
        column_number = i + 1
        print("| %s " %column_number, end = '')

    print("| ")
    print_row_break(board_dimensions.x)

    for i, row in enumerate(board):
        print("%s " %chr(65 + i), end='')

        for square in row:
            print("| %s " %square.symbol, end='')

        print("| ")
        print_row_break(board_dimensions.x)

    print("\n")

def print_row_break(row_length: int):
    dashes_per_column = 4
    print("-" * (row_length + 1) * dashes_per_column)