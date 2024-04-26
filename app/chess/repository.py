from .data import board_size
from .piece import Piece, PieceType
from .color import Color
from .vector import Vector


def get_starting_pieces():
    return set(
        piece
        for coordinates in (
            Vector(row, col) for row in range(board_size) for col in range(board_size)
        )
        if ((piece := get_starting_piece(coordinates)) is not None)
    )


def get_starting_piece(coordinates: Vector) -> Piece | None:
    row, col = coordinates

    color = Color.White if row in [0, 1] else Color.Black

    match row:
        case 1 | 6:
            return Piece(PieceType.Pawn, color, coordinates)

        case 0 | 7:
            match col:
                case 0 | 7:
                    return Piece(PieceType.Rook, color, coordinates)

                case 1 | 6:
                    return Piece(PieceType.Knight, color, coordinates)

                case 2 | 5:
                    return Piece(PieceType.Bishop, color, coordinates)

                case 3:
                    return Piece(PieceType.Queen, color, coordinates)

                case 4:
                    return Piece(PieceType.King, color, coordinates)

        case _:
            return None
