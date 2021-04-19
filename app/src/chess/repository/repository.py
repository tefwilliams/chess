
from typing import Callable, Iterable, TypeVar, Union
from ..data import board_size
from ..pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from ..player import Color
from ..coordinates import Coordinates


def get_starting_pieces() -> list[Piece]:
    pieces: list[Piece] = []

    for i in range(board_size):
        for j in range(board_size):
            coordinates = Coordinates(i, j)
            starting_piece = get_starting_piece(coordinates)

            if starting_piece:
                pieces.append(starting_piece)

    return pieces


def get_starting_piece(coordinates: Coordinates) -> Union[Piece, None]:
    # TODO - update this to use color direction
    color = Color.white if coordinates.y in [0, 1] else Color.black

    if coordinates.y in [1, 6]:
        return Pawn(coordinates, color)

    if coordinates.y in [0, 7]:
        if coordinates.x in [0, 7]:
            return Rook(coordinates, color)

        if coordinates.x in [1, 6]:
            return Knight(coordinates, color)

        if coordinates.x in [2, 5]:
            return Bishop(coordinates, color)

        if coordinates.x == 3:
            return Queen(coordinates, color)

        if coordinates.x == 4:
            return King(coordinates, color)
