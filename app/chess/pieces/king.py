
from __future__ import annotations
from typing import TYPE_CHECKING
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ..player import Color
    from ..coordinates import Coordinates
    from ..board import Board


class King(Piece):
    type = PieceTypes.king

    def __init__(self: King, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: King, board: Board) -> list[list[Coordinates]]:
        castle_moves = [squares_in_direction[1] for squares_in_direction in Movement.get_castle_squares(
            self.coordinates) if board.legal_castle(self, squares_in_direction[1])]

        return Movement.get_adjacent_squares(self.coordinates) + [castle_moves]
