from chess import (
    Board,
    Color,
    Move,
    Movement,
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


def create_move(origin: str, destination: str):
    return Move(
        Movement(
            to_coordinates(origin),
            to_coordinates(destination)
        )
    )


def create_en_passant_move(origin: str, destination: str, attack_location: str):
    return Move(
        Movement(
            to_coordinates(origin),
            to_coordinates(destination),
            to_coordinates(attack_location)
        )
    )


def to_coordinates(coordinates_as_string: str) -> Vector:
    assert len(coordinates_as_string) == 2

    col, row = coordinates_as_string

    return Vector(col_strings.index(col), row_strings.index(row))


def get_possible_destinations(square: Vector, board: Board):
    return {
        move.primary_movement.destination
        for move in board.get_possible_moves(square)
    }
