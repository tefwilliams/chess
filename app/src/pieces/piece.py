
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ...src.player import Color

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class Piece:
    def __init__(self: Piece, coordinates: Coordinates, color: Color) -> None:
        self.__color = color
        self.__coordinates = coordinates
        self.__has_moved = False
        self.__set_backup_data()

    def move(self: Piece, coordinates: Coordinates) -> None:
        self.__set_backup_data()
        self.__coordinates = coordinates
        self.__has_moved = True

    def update_possible_moves(self: Piece, board: Board) -> None:
        self.__possible_moves = self.get_possible_moves(board)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
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
    def possible_moves(self: Piece) -> list[Coordinates]:
        return self.__possible_moves

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
