
from __future__ import annotations
from typing import TYPE_CHECKING
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ..board import Board
    from ..coordinates import Coordinates
    from ..player import Color


class Bishop(Piece):
    type = PieceTypes.bishop

    def __init__(self: Bishop, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: Bishop, board: Board) -> list[list[Coordinates]]:
        return Movement.get_diagonal_squares(self.coordinates)
