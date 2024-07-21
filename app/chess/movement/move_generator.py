from copy import deepcopy

from .helpers import get_attacking_moves, get_non_attacking_moves
from ..board import Board, Move
from ..color import Color
from ..piece import Piece
from ..vector import Vector


class MoveGenerator:
    def __init__(self, board: Board) -> None:
        self.board = board

    def get_possible_moves(self, square: Vector) -> list[Move]:
        return [
            move
            for move in self.get_unobstructed_moves(square)
            if not self.__will_be_in_check_after_move(move)
        ]

    def get_unobstructed_moves(self, square: Vector) -> list[Move]:
        return self.get_attacking_moves(square) + self.get_non_attacking_moves(square)

    def get_attacking_moves(self, square: Vector) -> list[Move]:
        return get_attacking_moves(square, self.board)

    def get_non_attacking_moves(self, square: Vector) -> list[Move]:
        return get_non_attacking_moves(square, self.board)

    def __will_be_in_check_after_move(self, move: Move) -> bool:
        original_board = self.board

        # We want to copy the board
        # but keep the same instances of pieces
        # after the check has finished
        test_board = deepcopy(self.board)
        self.board = test_board

        self.board.move(move)
        in_check = self.in_check(move.primary_movement.piece.color)

        self.board = original_board
        return in_check

    def in_check(self, color: Color):
        return (
            king := self.board.get_king(color)
        ) is not None and self.__square_attacked(king.coordinates, color)

    def __square_attacked(self, square: Vector, color: Color) -> bool:
        return any(
            square
            in (
                move.primary_movement.attack_location
                for move in self.get_attacking_moves(piece)
            )
            for piece in self.board.pieces
            if piece.color != color
        )

    def any_possible_moves(self, color: Color) -> bool:
        return any(
            any(self.get_possible_moves(piece))
            for piece in self.board.pieces
            if piece.color == color
        )
