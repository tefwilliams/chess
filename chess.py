
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

generate_new_board()
