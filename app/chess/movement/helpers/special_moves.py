from .base_moves import get_pawn_attacking_moves
from .unit_steps import get_unit_step_backward
from ...board import Board, Move, Movement
from ...piece import Piece, PieceType
from ...shared import last
from ...vector import Vector


def get_castle_moves(square: Vector, board: Board) -> list[Move]:
    moves = []

    left_square = Vector(0, square.row)
    if valid_castle(square, left_square, board):
        moves.append(
            Move(
                Movement(square, Vector(2, square.row)),
                Movement(left_square, Vector(3, square.row)),
            )
        )

    right_square = Vector(7, square.row)
    if valid_castle(square, right_square, board):
        moves.append(
            Move(
                Movement(square, Vector(6, square.row)),
                Movement(right_square, Vector(5, square.row)),
            )
        )

    return moves


def valid_castle(king_square: Vector, rook_square: Vector, board: Board):
    return (
        # Don't need to verify type
        # or color as pieces haven't moved
        # TODO - king can't be in check
        board.try_get_piece(king_square) is not None
        (not king_square.has_moved)
        and (rook_square is not None and not rook_square.has_moved)
        and row_clear_between_cols(
            board,
            king_square.coordinates.row,
            min(king_square.coordinates.col, rook_square.coordinates.col),
            max(king_square.coordinates.col, rook_square.coordinates.col),
        )
        # TODO - king can't pass through attacked square (including current square)
    )


# TODO - maybe adapt to get square for row between cols
def row_clear_between_cols(board: Board, row: int, col_start: int, col_end: int):
    return not any(
        board.try_get_piece(coordinates)
        for coordinates in (Vector(col, row) for col in range(col_start + 1, col_end))
    )


def get_en_passant_moves(pawn: Piece, board: Board) -> list[Move]:
    return [
        Move(Movement(pawn, destination, attack_location))
        for move in get_pawn_attacking_moves(pawn, board, True)
        if valid_en_passant(
            pawn,
            board.try_get_piece(
                attack_location := (destination := move.primary_movement.destination)
                + get_unit_step_backward(pawn.color)
            ),
            board,
        )
    ]


def valid_en_passant(attacker: Piece, defender: Piece | None, board: Board):
    return (
        attacker.type == PieceType.Pawn
        and (defender and defender.type == PieceType.Pawn)
        and attacker.color != defender.color
        and defender == board.last_piece_to_move
        and has_just_moved_two_rows(defender)
    )


def has_just_moved_two_rows(piece: Piece):
    # TODO - must be on previous turn
    return (previous_coordinates := last(piece.coordinates_history)) and abs(
        piece.coordinates.row - previous_coordinates.row
    ) == 2
