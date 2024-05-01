from .base_moves import get_pawn_attacking_moves
from .unit_steps import get_unit_step_backward
from ...board import Board, Move, Movement
from ...piece import Piece, PieceType
from ...shared import last
from ...vector import Vector


def get_castle_moves(king: Piece, board: Board) -> list[Move]:
    moves = []

    # TODO - king can't be in check
    if king.has_moved:
        return moves

    left_rook = board.try_get_piece(Vector(0, king.coordinates.row))

    if valid_castle(king, left_rook, board):
        assert left_rook
        moves.append(
            Move(
                Movement(king, Vector(2, king.coordinates.row)),
                Movement(left_rook, Vector(3, king.coordinates.row)),
            )
        )

    right_rook = board.try_get_piece(Vector(7, king.coordinates.row))

    if valid_castle(king, right_rook, board):
        assert right_rook
        moves.append(
            Move(
                Movement(king, Vector(6, king.coordinates.row)),
                Movement(right_rook, Vector(5, king.coordinates.row)),
            )
        )

    return moves


def valid_castle(king: Piece, rook: Piece | None, board: Board):
    return (
        # Don't need to verify type
        # or color as pieces haven't moved
        (not king.has_moved)
        and (rook and not rook.has_moved)
        and row_clear_between_cols(
            board,
            king.coordinates.row,
            min(king.coordinates.col, rook.coordinates.col),
            max(king.coordinates.col, rook.coordinates.col),
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
