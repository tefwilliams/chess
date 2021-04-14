
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

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        castle_moves: list[Coordinates] = []
        adjacent_squares = Movement.get_adjacent_squares(self.coordinates)
        castle_squares = Movement.get_castle_squares(self.coordinates)

        for list_of_squares in castle_squares:
            piece_at_castle_position = board.get_piece(list_of_squares[-1])

            if (piece_at_castle_position
                and piece_at_castle_position.type == PieceTypes.rook
                and not self.has_moved
                and not piece_at_castle_position.has_moved
                and not board.is_in_check(self.color)
                and not any(board.square_is_attacked(square, self.color) for square in list_of_squares[0: 1])
                    and all(board.get_piece(square) is None for square in list_of_squares[0: -1])):
                castle_moves.append(list_of_squares[1])

        return castle_moves + board.get_valid_moves(self, adjacent_squares)
