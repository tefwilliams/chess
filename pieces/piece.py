
from __future__ import annotations
from enum import Enum
from player import Color
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coordinates import Coordinates
    from board import Board


class Piece:
    __color: Color
    __has_moved = False

    def __init__(self: Piece, coordinates: Coordinates) -> None:
        self.__color = Color.white if coordinates.y in [0, 1] else Color.black
        self.__coordinates = coordinates
        self.__set_backup_data()

    def move(self: Piece, coordinates: Coordinates) -> None:
        self.__set_backup_data()
        self.__coordinates = coordinates
        self.__has_moved = True

    def can_move(self: Piece, coordinates: Coordinates, board: Board) -> bool:
        raise NotImplementedError

    def restore(self: Piece) -> None:
        self.__coordinates, self.__has_moved = self.__backup_data

    def __set_backup_data(self: Piece,) -> None:
        self.__backup_data = self.__coordinates, self.has_moved

    @property
    def color(self: Piece) -> Color:
        return self.__color

    @property
    def coordinates(self: Piece) -> Coordinates:
        return self.__coordinates

    @property
    def has_moved(self: Piece) -> bool:
        return self.__has_moved

    @property
    def symbol(self: Piece) -> str:
        raise NotImplementedError

    @property
    def type(self: Piece) -> PieceTypes:
        raise NotImplementedError

class PieceTypes(Enum):
    king = 0
    queen = 1
    bishop = 2
    knight = 3
    rook = 4
    pawn = 5
