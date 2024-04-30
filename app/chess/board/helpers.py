from ..color import Color
from ..piece import PieceType, MovablePiece
from ..vector import Vector

board_size = 8


def get_starting_pieces():
    return set(
        piece
        for coordinates in (
            Vector(row, col) for row in range(board_size) for col in range(board_size)
        )
        if ((piece := get_starting_piece(coordinates)) is not None)
    )


def get_starting_piece(coordinates: Vector) -> MovablePiece | None:
    row, col = coordinates

    color = Color.White if row in [0, 1] else Color.Black

    match row:
        case 1 | 6:
            return MovablePiece(PieceType.Pawn, color, coordinates)

        case 0 | 7:
            match col:
                case 0 | 7:
                    return MovablePiece(PieceType.Rook, color, coordinates)

                case 1 | 6:
                    return MovablePiece(PieceType.Knight, color, coordinates)

                case 2 | 5:
                    return MovablePiece(PieceType.Bishop, color, coordinates)

                case 3:
                    return MovablePiece(PieceType.Queen, color, coordinates)

                case 4:
                    return MovablePiece(PieceType.King, color, coordinates)

        case _:
            return None


def within_board(coordinates: Vector):
    return 0 <= coordinates.row < board_size and 0 <= coordinates.col < board_size
