from typing import TYPE_CHECKING
from .base_moves import (
    get_bishop_attacking_moves,
    get_king_attacking_moves,
    get_knight_attacking_moves,
    get_pawn_attacking_moves,
    get_pawn_non_attacking_moves,
    get_queen_attacking_moves,
    get_rook_attacking_moves,
)
from .special_moves import get_en_passant_moves, get_castle_moves
from ..move import Move
from ...piece import PieceType
from ...vector import Vector

if TYPE_CHECKING:
    from ..board import Board


def get_attacking_moves(square: Vector, board: 'Board') -> list[Move]:
    match (piece := board.get_piece(square)).type:
        case PieceType.Pawn:
            return get_pawn_attacking_moves(square, piece.color, board) + get_en_passant_moves(
                square, piece.color, board
            )

        case PieceType.Rook:
            return get_rook_attacking_moves(square, piece.color, board)

        case PieceType.Knight:
            return get_knight_attacking_moves(square, piece.color, board)

        case PieceType.Bishop:
            return get_bishop_attacking_moves(square, piece.color, board)

        case PieceType.Queen:
            return get_queen_attacking_moves(square, piece.color, board)

        case PieceType.King:
            return get_king_attacking_moves(square, piece.color, board)


def get_non_attacking_moves(square: Vector, board: 'Board') -> list[Move]:
    match (piece := board.get_piece(square)).type:
        case PieceType.Pawn:
            return get_pawn_non_attacking_moves(square, piece.color, board)

        case PieceType.King:
            return get_castle_moves(square, board)

        case _:
            return []
