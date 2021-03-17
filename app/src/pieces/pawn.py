
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates, Direction
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.board import Board


class Pawn(Piece):
    def __init__(self: Pawn, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2659' if self.color == Color.white else '\u265F'

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        possible_moves: list[list[Coordinates]] = []
        vertical_direction = 1 if self.color == Color.white else -1

        squares = Movement.get_pawn_squares(self.coordinates, vertical_direction, self.has_moved)
        attack_squares = Movement.get_pawn_attack_squares(self.coordinates, vertical_direction)

        for list_of_squares in squares:
            possible_moves.append([square for square in list_of_squares if not board.get_piece(square)])

        for list_of_squares in attack_squares:
            possible_moves.append([square for square in list_of_squares if board.get_piece(square)])

        return board.get_unobstructed_squares(self.color, possible_moves)

    @property
    def type(self: Pawn) -> PieceTypes:
        return PieceTypes.pawn
