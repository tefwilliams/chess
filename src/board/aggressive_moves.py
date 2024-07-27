from typing import Callable, Iterable
from .board import Board
from .helpers import (
    unit_step_left,
    unit_step_right,
    orthogonal_unit_steps,
    diagonal_unit_steps,
    get_squares_until_blocked,
    get_unit_step_forward,
    pawn_attacking_square_blocked_callback,
    attacking_square_blocked_callback,
)
from .move import Move, Movement
from ..piece import PieceType
from ..vector import Vector


class AggressiveMoves:
    def __init__(self, board: Board) -> None:
        self.__board = board

    def get_moves(self, square: Vector):
        return (
            Move(Movement(square, destination))
            for step in self.__get_unit_steps(square)
            for destination in get_squares_until_blocked(
                self.__get_square_blocked_callback(square),
                square,
                step,
                self.__get_max_number_steps(square),
            )
        )

    def __get_unit_steps(self, initial_square: Vector) -> Iterable[Vector]:
        match (piece := self.__board.get_piece(initial_square)).type:
            case PieceType.Pawn:
                return (
                    get_unit_step_forward(piece.color) + step
                    for step in (unit_step_left, unit_step_right)
                )

            case PieceType.Rook:
                return orthogonal_unit_steps

            case PieceType.Knight:
                return (
                    step
                    for orthogonal_step in orthogonal_unit_steps
                    for diagonal_step in diagonal_unit_steps
                    if abs((step := orthogonal_step + diagonal_step).row)
                    + abs(step.col)
                    == 3
                )

            case PieceType.Bishop:
                return diagonal_unit_steps

            case PieceType.Queen | PieceType.King:
                return diagonal_unit_steps + orthogonal_unit_steps

    def __get_square_blocked_callback(
        self, initial_square: Vector
    ) -> Callable[[Vector, Vector | None], bool]:
        match (piece := self.__board.get_piece(initial_square)).type:
            case PieceType.Pawn:
                return pawn_attacking_square_blocked_callback(self.__board, piece.color)

            case _:
                return attacking_square_blocked_callback(self.__board, piece.color)

    def __get_max_number_steps(self, initial_square: Vector) -> int | None:
        match self.__board.get_piece(initial_square).type:
            case PieceType.Pawn | PieceType.Knight | PieceType.King:
                return 1

            case _:
                return None
