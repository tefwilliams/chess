from .unit_steps import (
    get_unit_step_forward,
    unit_step_left,
    unit_step_right,
    orthogonal_unit_steps,
    diagonal_unit_steps,
)
from .helpers import (
    get_squares_until_blocked,
    attacking_square_blocked_callback,
    non_attacking_square_blocked_callback,
    pawn_attacking_square_blocked_callback
)
from ...board import Move, Movement
from ...color import Color
from ...board import Board
from ...vector import Vector


# ------------- PAWN -------------


def get_pawn_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in (unit_step_left, unit_step_right)
        for destination in get_squares_until_blocked(
            pawn_attacking_square_blocked_callback(board, color),
            square,
            get_unit_step_forward(color) + step,
            1,
        )
    ]


def get_pawn_non_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for destination in get_squares_until_blocked(
            non_attacking_square_blocked_callback(board, color),
            square,
            get_unit_step_forward(color),
            1 if board.piece_at_square_has_moved(square) else 2,
        )
    ]


# ------------- ROOK -------------


def get_rook_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, color),
            square,
            step,
        )
    ]


# ------------- Knight -------------


def get_knight_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in (
            orthogonal_step + diagonal_step
            for orthogonal_step in orthogonal_unit_steps
            for diagonal_step in diagonal_unit_steps
        )
        if abs(step.row) + abs(step.col) == 3
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, color),
            square,
            step,
            1,
        )
    ]


# ------------- Bishop -------------


def get_bishop_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in diagonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, color),
            square,
            step,
        )
    ]


# ------------- Queen -------------


def get_queen_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in diagonal_unit_steps + orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, color),
            square,
            step,
        )
    ]


# ------------- King -------------


def get_king_attacking_moves(square: Vector, color: Color, board: Board) -> list[Move]:
    return [
        Move(Movement(square, destination))
        for step in diagonal_unit_steps + orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, color),
            square,
            step,
            1,
        )
    ]
