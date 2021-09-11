
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...chess.coordinates import Coordinates
    from ...chess.board import Board


class Rook(Piece):
    type = PieceTypes.rook

    def __init__(self: Rook, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: Rook, board: Board) -> list[list[Coordinates]]:
        return Movement.get_orthogonal_squares(self.coordinates)
