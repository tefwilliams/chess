
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class Rook(Piece):
    def __init__(self: Rook, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2656' if self.color == Color.white else '\u265C'

    @property
    def symbol(self: Rook) -> str:
        return self.__symbol

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        orthogonal_squares = Movement.get_orthogonal_squares(self.coordinates)
        return board.get_unobstructed_squares(self.color, orthogonal_squares)

    @property
    def type(self: Rook) -> PieceTypes:
        return PieceTypes.rook
