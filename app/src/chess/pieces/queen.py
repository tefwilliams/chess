
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...chess.coordinates import Coordinates
    from ...chess.board import Board


class Queen(Piece):
    type = PieceTypes.queen

    def __init__(self: Queen, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        diagonal_squares = Movement.get_diagonal_squares(self.coordinates)
        orthogonal_squares = Movement.get_orthogonal_squares(self.coordinates)
        return board.get_unobstructed_squares(self.color, diagonal_squares + orthogonal_squares)
