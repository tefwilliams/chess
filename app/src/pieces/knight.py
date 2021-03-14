
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class Knight(Piece):
    def __init__(self: Knight, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2658' if self.color == Color.white else '\u265E'

    @property
    def symbol(self: Knight) -> str:
        return self.__symbol

    def can_move(self: Knight, coordinates: Coordinates, *args) -> bool:
        return Movement.is_knight(self.coordinates, coordinates)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        knight_squares = Movement.get_knight_squares(self.coordinates)
        return board.get_unobstructed_squares(self, knight_squares)

    @property
    def type(self: Knight) -> PieceTypes:
        return PieceTypes.knight
