
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

def print_board(board: list[list[Square]]) -> None:
    board_icons: list[list[str]] = []

    for row in board:
        row_icons: list[str] = []

        for square in row:
            try:
                row_icons.append(square.piece_symbol)

            except AttributeError:
                row_icons.append(' ')

        board_icons.append(row_icons)

    print(board_icons)

print_board(board)

