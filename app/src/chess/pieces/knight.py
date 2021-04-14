
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...chess.coordinates import Coordinates
    from ...chess.board import Board


class Knight(Piece):
    type = PieceTypes.knight

    def __init__(self: Knight, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        knight_squares = Movement.get_knight_squares(self.coordinates)
        return board.get_unobstructed_squares(self.color, knight_squares)
