
from app.src import Pawn, Coordinates, Board


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    coordinates = Coordinates((1, 2))
    piece = Pawn(coordinates)

    board = Board([piece])

    assert board.get_piece(coordinates) == piece
