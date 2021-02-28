
from ...src.pieces import Piece, Pieces
from ...src.coordinates import Coordinates
from ...src.board import Board


def display_board(board: Board) -> None:
    print("\n")
    print_column_numbers()
    print_row_break()

    for row_number in range(Board.shape.y):
        print_row_start_letter(row_number)
        print_row_squares(row_number, board)
        print_row_end_letter(row_number)
        print_row_break()

    print_column_numbers()
    print("\n")

def print_row_break() -> None:
    row_length = Board.shape.x
    dashes_per_column = 4
    print("-" * ((row_length + 2) * dashes_per_column - 1))

def print_column_numbers() -> None:
    print_row_start()
    row_length = Board.shape.x

    for i in range(row_length):
        column_number = Coordinates.x_grid_values[i]
        print("| %s " % column_number, end = '')

    print_row_end()

def print_row_start() -> None:
    print("   ", end = '')

def print_row_end() -> None:
    print("| ")

def print_row_start_letter(row_number: int) -> None:
    print(" %s " % Coordinates.y_grid_values[row_number], end='')

def print_row_end_letter(row_number: int) -> None:
    print("| %s" % Coordinates.y_grid_values[row_number])

def print_row_squares(row_number: int, board: Board) -> None:
    row_length = Board.shape.x

    for column_number in range(row_length):
        coordinates = Coordinates((row_number, column_number))
        piece = board.get_piece(coordinates)

        symbol = piece.symbol if piece else " "
        print("| %s " % symbol, end='')

def get_starting_pieces() -> list[Piece]:
    board_dimensions = Board.shape
    pieces: list[Piece] = []

    for i in range(board_dimensions.y):
        for j in range(board_dimensions.x):
            coordinates = Coordinates((i, j))
            starting_piece = Pieces.get_starting_piece(coordinates)
            
            if starting_piece:
                pieces.append(starting_piece)

    return pieces