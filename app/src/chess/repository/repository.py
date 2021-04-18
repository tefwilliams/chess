
from typing import Callable, Iterable, TypeVar
from ..data import board_size
from ..pieces import Piece, Pieces
from ..coordinates import Coordinates


def get_starting_pieces() -> list[Piece]:
    pieces: list[Piece] = []

    for i in range(board_size):
        for j in range(board_size):
            coordinates = Coordinates(i, j)
            starting_piece = Pieces.get_starting_piece(coordinates)

            if starting_piece:
                pieces.append(starting_piece)

    return pieces


T = TypeVar('T')


def each(function: Callable[[T], None], iterable: Iterable[T]) -> None:
    for item in iterable:
        function(item)
