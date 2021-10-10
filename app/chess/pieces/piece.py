
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ..helpers import last

if TYPE_CHECKING:
    from ..color import Color
    from ..grid import Coordinates
    from ..board import Board


class Piece:
    type: PieceTypes

    def __init__(self: Piece, coordinates: Coordinates, color: Color) -> None:
        self.__color = color
        self.__coordinates = coordinates
        # TODO - maybe make this a list of coordinates, since we can work out the moves from that
        # also need to record what turn a move was made on
        self.__positions: list[Coordinates] = []

    @property
    def color(self: Piece) -> Color:
        return self.__color

    @property
    def coordinates(self: Piece) -> Coordinates:
        return self.__coordinates

    @property
    def previous_coordinates(self: Piece) -> Coordinates | None:
        return last(self.__positions)

    @property
    def has_moved(self: Piece) -> bool:
        return self.previous_coordinates is not None

    def move(self: Piece, new_coordinates: Coordinates) -> None:
        self.__positions.append(self.coordinates)
        self.__coordinates = new_coordinates

    def get_base_moves(self: Piece, board: Board) -> list[list[Coordinates]]:
        raise NotImplementedError


class PieceTypes(Enum):
    king = 0
    queen = 1
    bishop = 2
    knight = 3
    rook = 4
    pawn = 5
