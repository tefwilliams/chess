from chess import (
    Board,
    Color,
    Move,
    Movement,
    MoveGenerator,
    MovablePiece,
    PieceType,
    Piece,
    Vector,
)

col_strings = ["A", "B", "C", "D", "E", "F", "G", "H"]
row_strings = ["8", "7", "6", "5", "4", "3", "2", "1"]


def create_pieces(pieces: list[tuple[PieceType, str, Color]]) -> dict[Vector, Piece]:
    return {
        to_coordinates(coordinates_as_string): Piece(type, color)
        for type, coordinates_as_string, color in pieces
    }


def create_move(*movements: tuple[MovablePiece, str]):
    return Move(
        *(
            Movement(piece, to_coordinates(coordinates_as_string))
            for piece, coordinates_as_string in movements
        )
    )


def to_coordinates(coordinates_as_string: str) -> Vector:
    assert len(coordinates_as_string) == 2

    col, row = coordinates_as_string

    return Vector(col_strings.index(col), row_strings.index(row))


def get_possible_destinations(piece: MovablePiece, board: Board):
    return {
        move.primary_movement.destination
        for move in MoveGenerator(board).get_possible_moves(piece)
    }
