
from __future__ import annotations
from typing import TYPE_CHECKING
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ..color import Color
    from ..grid import Coordinates
    from ..board import Board


class Queen(Piece):
    type = PieceTypes.queen

    def __init__(self: Queen, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: Queen, board: Board) -> list[list[Coordinates]]:
        return Movement.get_diagonal_squares(self.coordinates) + Movement.get_orthogonal_squares(self.coordinates)
