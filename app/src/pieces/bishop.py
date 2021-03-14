
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.board import Board


class Bishop(Piece):
    def __init__(self: Bishop, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2657' if self.color == Color.white else '\u265D'

    @property
    def symbol(self: Bishop) -> str:
        return self.__symbol

    def can_move(self: Bishop, coordinates: Coordinates, board) -> bool:
        return Movement.is_diagonal(self.coordinates, coordinates)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        diagonal_squares = Movement.get_diagonal_squares(self.coordinates)
        return board.get_unobstructed_squares(self, diagonal_squares)

    @property
    def type(self: Bishop) -> PieceTypes:
        return PieceTypes.bishop
        