from chess import (
    Board,
    Move,
    Movement,
    Piece,
    Vector,
)

col_strings = ["A", "B", "C", "D", "E", "F", "G", "H"]
row_strings = ["8", "7", "6", "5", "4", "3", "2", "1"]


def create_board(pieces: dict[str, Piece]) -> Board:
    return Board({to_coordinates(square): piece for square, piece in pieces.items()})


def create_move(origin: str, destination: str):
    return Move(Movement(to_coordinates(origin), to_coordinates(destination)))


def create_en_passant_move(origin: str, destination: str, attack_location: str):
    return Move(
        Movement(
            to_coordinates(origin),
            to_coordinates(destination),
            to_coordinates(attack_location),
        )
    )


def to_coordinates(coordinates_as_string: str) -> Vector:
    assert len(coordinates_as_string) == 2

    col, row = coordinates_as_string

    return Vector(col_strings.index(col), row_strings.index(row))


def to_grid_string(coordinates: Vector) -> str:
    return col_strings[coordinates.col] + row_strings[coordinates.row]


def get_possible_destinations(square: str, board: Board) -> list[str]:
    return sorted(
        to_grid_string(move.primary_movement.destination)
        for move in board.get_possible_moves(to_coordinates(square))
    )
