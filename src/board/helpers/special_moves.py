from typing import TYPE_CHECKING
from .helpers import get_squares_until_blocked, non_attacking_square_blocked_callback
from .unit_steps import (
    unit_step_left,
    unit_step_right,
    get_unit_step_forward,
    get_unit_step_backward,
)
from ..move import Move
from ..movement import Movement
from ...color import Color
from ...piece import PieceType
from ...vector import Vector

if TYPE_CHECKING:
    from ..board import Board


def get_castle_moves(square: Vector, board: "Board") -> list[Move]:
    return [
        Move(
            Movement(square, Vector(king_destination_col, square.row)),
            Movement(rook_origin, Vector(rook_destination_col, square.row)),
        )
        for rook_origin_col, king_destination_col, rook_destination_col in (
            (0, 2, 3),
            (7, 6, 5),
        )
        if valid_castle(
            square, rook_origin := Vector(rook_origin_col, square.row), board
        )
    ]


def valid_castle(king_square: Vector, rook_square: Vector, board: "Board"):
    return (
        (king := board.get_piece(king_square))
        and king.type == PieceType.King
        and (rook := board.try_get_piece(rook_square))
        and rook.type == PieceType.Rook
        and king.color == rook.color
        and not board.piece_at_square_has_moved(king_square)
        and not board.piece_at_square_has_moved(rook_square)
        and row_clear_between_cols(
            board,
            king_square.row,
            min(king_square.col, rook_square.col),
            max(king_square.col, rook_square.col),
        )
        # King can't pass through attacked square
        and row_not_attacked_between_cols(
            board,
            king_square.row,
            king_square.col - (3 if rook_square.col < king_square.col else 1),
            king_square.col + (1 if rook_square.col < king_square.col else 3),
            king.color,
        )
    )


# TODO - maybe adapt to get square for row between cols
def row_clear_between_cols(board: "Board", row: int, col_start: int, col_end: int):
    return not any(
        board.try_get_piece(coordinates)
        for coordinates in (Vector(col, row) for col in range(col_start + 1, col_end))
    )


def row_not_attacked_between_cols(
    board: "Board", row: int, col_start: int, col_end: int, color: Color
):
    return not any(
        board.square_attacked(coordinates, color)
        for coordinates in (Vector(col, row) for col in range(col_start + 1, col_end))
    )


def get_en_passant_moves(square: Vector, color: Color, board: "Board") -> list[Move]:
    return [
        move
        for step in (unit_step_left, unit_step_right)
        for destination in get_squares_until_blocked(
            non_attacking_square_blocked_callback(board, color),
            square,
            get_unit_step_forward(color) + step,
            1,
        )
        if valid_en_passant(
            move := Move(
                Movement(
                    square, destination, destination + get_unit_step_backward(color)
                )
            ),
            board,
        )
    ]


def valid_en_passant(move: Move, board: "Board"):
    return (
        # Destination is clear due to non_attacking_square_blocked_callback
        (attacker := board.get_piece(move.primary_movement.origin)).type
        == PieceType.Pawn
        and (
            (
                defender := board.try_get_piece(
                    defender_location := move.primary_movement.attack_location
                )
            )
            and defender.type == PieceType.Pawn
        )
        and attacker.color != defender.color
        # Defender is last piece to move
        and (last_move := board.get_last_move())
        and last_move.primary_movement.destination == defender_location
        # Defender just moved two rows
        and abs(
            last_move.primary_movement.origin.row
            - last_move.primary_movement.destination.row
        )
        == 2
    )
