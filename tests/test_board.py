import src
from tests.data.generate_board import generate_board

def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    coordinates = src.Coordinates((1, 2))
    piece = src.pieces.Pawn(coordinates)

    board = generate_board([piece])

    assert board.get_piece(coordinates) == piece

test_get_piece_returns_piece_with_specified_coordinates()
