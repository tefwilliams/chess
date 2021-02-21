
from coordinates import Coordinates
from board import Board

# TODO - add letters/numbers to other sides
def display_board(board: Board) -> None:
    board_dimensions = Board.shape

    print("\n" + "  ", end = '')

    for i in range(board_dimensions.x):
        column_number = Coordinates.x_grid_values[i]
        print("| %s " % column_number, end = '')

    print("| ")
    print_row_break(board_dimensions.x)

    for i in range(board_dimensions.y):
        print("%s " % Coordinates.y_grid_values[i], end='')

        for j in range(board_dimensions.x):
            coordinates = Coordinates((i, j))
            piece = board.get_piece(coordinates)

            symbol = piece.symbol if piece else " "
            print("| %s " % symbol, end='')

        print("| ")
        print_row_break(board_dimensions.x)

    print("\n")

def print_row_break(row_length: int):
    dashes_per_column = 4
    print("-" * (row_length + 1) * dashes_per_column)
