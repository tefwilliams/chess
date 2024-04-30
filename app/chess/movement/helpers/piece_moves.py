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
from ...board import Board
from ...piece import Piece, PieceType


def get_attacking_moves(piece: Piece, board: Board):
    match piece.type:
        case PieceType.Pawn:
            return get_pawn_attacking_moves(piece, board) + get_en_passant_moves(
                piece, board
            )

        case PieceType.Rook:
            return get_rook_attacking_moves(piece, board)

        case PieceType.Knight:
            return get_knight_attacking_moves(piece, board)

        case PieceType.Bishop:
            return get_bishop_attacking_moves(piece, board)

        case PieceType.Queen:
            return get_queen_attacking_moves(piece, board)

        case PieceType.King:
            return get_king_attacking_moves(piece, board)


def get_non_attacking_moves(piece: Piece, board: Board):
    match piece.type:
        case PieceType.Pawn:
            return get_pawn_non_attacking_moves(piece, board)

        case PieceType.King:
            return get_castle_moves(piece, board)

        case _:
            return []
