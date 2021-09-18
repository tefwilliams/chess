
from __future__ import annotations
from typing import TYPE_CHECKING
from ..movement import Movement
from ..coordinates import Coordinates
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ..board import Board
    from ..player import Color


class Pawn(Piece):
    type = PieceTypes.pawn

    def __init__(self: Pawn, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: Pawn, board: Board) -> list[list[Coordinates]]:
        return [
            [move for moves_in_direction in Movement.get_pawn_squares(
                self.coordinates, self.color, self.has_moved) for move in moves_in_direction if not board.get_piece(move)],
            [move for moves_in_direction in Movement.get_pawn_attack_squares(
                self.coordinates, self.color) for move in moves_in_direction if board.get_piece(move) or board.legal_en_passant(self, move)]
        ]
