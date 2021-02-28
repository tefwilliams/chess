
from app.src.pieces.pawn import Pawn
from app.src.coordinates import Coordinates
from .data.generate_board import generate_board


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    coordinates = Coordinates((1, 2))
    piece = Pawn(coordinates)

    board = generate_board([piece])

    assert board.get_piece(coordinates) == piece
