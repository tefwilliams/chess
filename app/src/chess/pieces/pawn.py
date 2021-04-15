
from __future__ import annotations
from typing import TYPE_CHECKING
from ..player import Color
from ..movement import Movement
from ..coordinates import Coordinates
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...chess.board import Board


class Pawn(Piece):
    type = PieceTypes.pawn

    def __init__(self: Pawn, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        possible_moves: list[list[Coordinates]] = []

        squares = Movement.get_pawn_squares(
            self.coordinates, self.color, self.has_moved)
        attack_squares = Movement.get_pawn_attack_squares(
            self.coordinates, self.color)

        for list_of_squares in squares:
            possible_moves.append(
                [square for square in list_of_squares if not board.get_piece(square)])

        for list_of_squares in attack_squares:
            possible_moves.append([square for square in list_of_squares if board.get_piece(
                square) or board.en_passant_valid(square, self.color)])

        return board.get_legal_moves(self, possible_moves)
