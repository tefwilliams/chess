from typing import Callable
from .aggressive_moves import AggressiveMoves
from .board import Board
from .helpers import (
    get_squares_until_blocked,
    non_attacking_square_blocked_callback,
    get_unit_step_forward,
)
from .move import Move, Movement
from ..color import Color
from ..piece import PieceType
from ..shared import has_two_items
from ..vector import Vector


class PassiveMoves:
    def __init__(
        self, board: Board, aggressive_move_generator: AggressiveMoves
    ) -> None:
        self.__board = board
        self.__aggressive_move_generator = aggressive_move_generator

    def get_moves(self, square: Vector):
        match (piece := self.__board.get_piece(square)).type:
            case PieceType.Pawn:
                return self.__get_pawn_passive_moves(square, piece.color)

            case PieceType.King:
                return self.__get_castle_moves(square)

            case _:
                return []

    # ------------- PAWN -------------

    def __get_pawn_passive_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for destination in get_squares_until_blocked(
                non_attacking_square_blocked_callback(self.__board, color),
                square,
                get_unit_step_forward(color),
                1 if self.__board.piece_at_square_has_moved(square) else 2,
            )
        ]

    # ------------- KING -------------

    def __get_castle_moves(self, square: Vector) -> list[Move]:
        return [
            move
            for rook_origin_col, king_destination_col, rook_destination_col in (
                (0, 2, 3),
                (7, 6, 5),
            )
            if self.__valid_castle(
                move := Move(
                    Movement(square, Vector(king_destination_col, square.row)),
                    Movement(
                        Vector(rook_origin_col, square.row),
                        Vector(rook_destination_col, square.row),
                    ),
                )
            )
        ]

    # ------------- Helpers -------------

    def __valid_castle(self, move: Move):
        if not has_two_items(move.movements):
            return False

        king_move, rook_move = move.movements

        return (
            (
                (king := self.__board.get_piece(king_move.origin))
                and king.type == PieceType.King
                and not self.__board.piece_at_square_has_moved(king_move.origin)
                and not self.__aggressive_move_generator.square_attacked(
                    king_move.origin, king.color
                )
            )
            and (
                (rook := self.__board.try_get_piece(rook_move.origin))
                and rook.type == PieceType.Rook
                and not self.__board.piece_at_square_has_moved(rook_move.origin)
            )
            and king.color == rook.color
            # Space between king and rook clear
            and row_meets_condition_between_cols(
                lambda coordinates: not self.__board.try_get_piece(coordinates),
                king_move.origin.row,
                min(king_move.origin.col, rook_move.origin.col),
                max(king_move.origin.col, rook_move.origin.col),
            )
            # King can't pass through attacked square
            and row_meets_condition_between_cols(
                lambda coordinates: not self.__aggressive_move_generator.square_attacked(
                    coordinates, king.color
                ),
                king_move.origin.row,
                min(king_move.origin.col, king_move.destination.col),
                max(king_move.origin.col, king_move.destination.col),
            )
        )


def row_meets_condition_between_cols(
    condition: Callable[[Vector], bool],
    row: int,
    col_start: int,
    col_end: int,
):
    return all(condition(Vector(col, row)) for col in range(col_start + 1, col_end))
