from ..piece import Piece, PieceType


def get_moves(piece: Piece):
    match piece.type:
        case PieceType.Pawn:
            return
