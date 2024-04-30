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
    enemy_piece_at_square,
)
from ...board.move import Move
from ...board.movement import Movement
from ...piece import Piece, PieceType
from ...board import Board


# ------------- PAWN -------------


def get_pawn_attacking_moves(pawn: Piece, board: Board, en_passant=False) -> list[Move]:
    assert pawn.type == PieceType.Pawn
    return [
        Move(Movement(pawn, destination))
        for step in (unit_step_left, unit_step_right)
        for destination in get_squares_until_blocked(
            lambda current_square, last_square: (
                attacking_square_blocked_callback(board, pawn.color)(
                    current_square, last_square
                )
                or not (
                    en_passant
                    or enemy_piece_at_square(current_square, pawn.color, board)
                )
            ),
            pawn.coordinates,
            get_unit_step_forward(pawn.color) + step,
            1,
        )
    ]


def get_pawn_non_attacking_moves(pawn: Piece, board: Board) -> list[Move]:
    assert pawn.type == PieceType.Pawn
    return [
        Move(Movement(pawn, destination))
        for destination in get_squares_until_blocked(
            non_attacking_square_blocked_callback(board, pawn.color),
            pawn.coordinates,
            get_unit_step_forward(pawn.color),
            1 if pawn.has_moved else 2,
        )
    ]


# ------------- ROOK -------------


def get_rook_attacking_moves(rook: Piece, board: Board) -> list[Move]:
    assert rook.type == PieceType.Rook
    return [
        Move(Movement(rook, destination))
        for step in orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, rook.color),
            rook.coordinates,
            step,
        )
    ]


# ------------- Knight -------------


def get_knight_attacking_moves(knight: Piece, board: Board) -> list[Move]:
    assert knight.type == PieceType.Knight
    return [
        Move(Movement(knight, destination))
        for step in (
            orthogonal_step + diagonal_step
            for orthogonal_step in orthogonal_unit_steps
            for diagonal_step in diagonal_unit_steps
        )
        if abs(step.row) + abs(step.col) == 3
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, knight.color),
            knight.coordinates,
            step,
            1,
        )
    ]


# ------------- Bishop -------------


def get_bishop_attacking_moves(bishop: Piece, board: Board) -> list[Move]:
    assert bishop.type == PieceType.Bishop
    return [
        Move(Movement(bishop, destination))
        for step in diagonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, bishop.color),
            bishop.coordinates,
            step,
        )
    ]


# ------------- Queen -------------


def get_queen_attacking_moves(queen: Piece, board: Board) -> list[Move]:
    assert queen.type == PieceType.Queen
    return [
        Move(Movement(queen, destination))
        for step in diagonal_unit_steps + orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, queen.color),
            queen.coordinates,
            step,
        )
    ]


# ------------- King -------------


def get_king_attacking_moves(king: Piece, board: Board) -> list[Move]:
    assert king.type == PieceType.King
    return [
        Move(Movement(king, destination))
        for step in diagonal_unit_steps + orthogonal_unit_steps
        for destination in get_squares_until_blocked(
            attacking_square_blocked_callback(board, king.color),
            king.coordinates,
            step,
            1,
        )
    ]
