
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class Queen(Piece):
    def __init__(self: Queen, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2655' if self.color == Color.white else '\u265B'

    @property
    def symbol(self: Queen) -> str:
        return self.__symbol

    def can_move(self: Queen, coordinates: Coordinates, *args) -> bool:
        return (Movement.is_horizontal(self.coordinates, coordinates) 
            or Movement.is_vertical(self.coordinates, coordinates) 
            or Movement.is_diagonal(self.coordinates, coordinates))

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        diagonal_squares = Movement.get_diagonal_squares(self.coordinates)
        orthogonal_squares = Movement.get_orthogonal_squares(self.coordinates)
        return board.get_unobstructed_squares(self, diagonal_squares + orthogonal_squares)

    @property
    def type(self: Queen) -> PieceTypes:
        return PieceTypes.queen
