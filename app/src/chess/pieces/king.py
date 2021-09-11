
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...chess.coordinates import Coordinates
    from ...chess.board import Board


class King(Piece):
    type = PieceTypes.king

    def __init__(self: King, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_base_moves(self: King, board: Board) -> list[list[Coordinates]]:
        castle_moves: list[Coordinates] = []
        adjacent_squares = Movement.get_adjacent_squares(self.coordinates)
        castle_squares = Movement.get_castle_squares(self.coordinates)

        for list_of_squares in castle_squares:
            if board.legal_castle(self, list_of_squares[1]):
                castle_moves.append(list_of_squares[1])

        return adjacent_squares + [castle_moves]
