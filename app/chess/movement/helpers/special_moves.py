from .unit_steps import get_unit_step_backward
from .piece_moves import get_pawn_attacking_moves
from ...board import Board, Move, Movement
from ...piece import Piece, PieceType
from ...shared import last
from ...vector import Vector


def get_castle_moves(king: Piece, board: Board) -> list[Move]:
    moves = []

    # TODO - king can't be in check
    if king.has_moved:
        return moves

    left_rook = board.try_get_piece(Vector(king.coordinates.row, 0))

    if valid_castle(king, left_rook, board):
        assert left_rook
        moves.append(
            Move(
                Movement(king, Vector(king.coordinates.row, 2)),
                Movement(left_rook, Vector(king.coordinates.row, 3)),
            )
        )

    right_rook = board.try_get_piece(Vector(king.coordinates.row, 7))

    if valid_castle(king, right_rook, board):
        assert right_rook
        moves.append(
            Move(
                Movement(king, Vector(king.coordinates.row, 6)),
                Movement(right_rook, Vector(king.coordinates.row, 5)),
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
            king.coordinates.col,
            # TODO - need to get min and max col correct
            rook.coordinates.col,
        )
        # TODO - king can't pass through attacked square (including current square)
    )


# TODO - maybe adapt to get square for row between cols
def row_clear_between_cols(board: Board, row: int, col_start: int, col_end: int):
    return not any(
        board.get_piece(coordinates)
        for coordinates in (Vector(row, col) for col in range(col_start + 1, col_end))
    )


def get_en_passant_moves(pawn: Piece, board: Board) -> list[Move]:
    return [
        Move(Movement(pawn, destination, attack_location))
        for move in get_pawn_attacking_moves(pawn, board)
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
    return (previous_coordinates := last(piece.coordinates_history)) and abs(
        piece.coordinates.row - previous_coordinates.row
    ) == 2
