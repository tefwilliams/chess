from ..color import Color
from ..piece import PieceType, Piece
from ..vector import Vector

board_size = 8


def get_starting_pieces():
    return {
        coordinates: piece
        for coordinates in (
            Vector(col, row) for row in range(board_size) for col in range(board_size)
        )
        if ((piece := get_starting_piece(coordinates)) is not None)
    }


def get_starting_piece(coordinates: Vector) -> Piece | None:
    # White starts at the bottom of the board
    color = Color.White if coordinates.row in [6, 7] else Color.Black

    match coordinates.row:
        case 1 | 6:
            return Piece(PieceType.Pawn, color)

        case 0 | 7:
            match coordinates.col:
                case 0 | 7:
                    return Piece(PieceType.Rook, color)

                case 1 | 6:
                    return Piece(PieceType.Knight, color)

                case 2 | 5:
                    return Piece(PieceType.Bishop, color)

                case 3:
                    return Piece(PieceType.Queen, color)

                case 4:
                    return Piece(PieceType.King, color)

        case _:
            return None


def within_board(coordinates: Vector):
    return 0 <= coordinates.row < board_size and 0 <= coordinates.col < board_size
