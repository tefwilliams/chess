
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class King(Piece):
    type = PieceTypes.king

    def __init__(self: King, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2654' if self.color == Color.white else '\u265A'

    @property
    def symbol(self: King) -> str:
        return self.__symbol

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        adjacent_squares = Movement.get_adjacent_squares(self.coordinates)
        return board.get_unobstructed_squares(self.color, adjacent_squares)
        