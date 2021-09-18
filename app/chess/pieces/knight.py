
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ..coordinates import Coordinates
    from ..board import Board


class Knight(Piece):
    type = PieceTypes.knight

    def __init__(self: Knight, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: Knight, board: Board) -> list[list[Coordinates]]:
        return Movement.get_knight_squares(self.coordinates)
