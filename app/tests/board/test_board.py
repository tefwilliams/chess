
import pytest
from app.src import PieceTypes, Coordinates, Board, Color
from app.tests.data.generate_piece import generate_piece


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    piece = generate_piece(PieceTypes.pawn, 'A1', Color.white)
    get_from_coordinates = Coordinates.convert_from_grid_value('A1') 

    board = Board([piece])

    assert board.get_piece(get_from_coordinates) == piece

def test_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    piece = generate_piece(PieceTypes.pawn, 'A1', Color.white)
    get_from_coordinates = Coordinates.convert_from_grid_value('B1')

    board = Board([piece])

    assert board.get_piece(get_from_coordinates) == None

@pytest.mark.parametrize(
    "black_piece, piece_coordinates", 
    [
        (PieceTypes.queen, 'A1'),
        (PieceTypes.queen, 'F4'),
        (PieceTypes.bishop, 'F2'),
        (PieceTypes.rook, 'D8'),
        (PieceTypes.knight, 'B3'),
        (PieceTypes.pawn, 'E5')
    ]
)
def test_is_in_check_returns_true_when_king_in_check(black_piece, piece_coordinates) -> None:
    pieces = [
        generate_piece(PieceTypes.king, 'D4', Color.white),
        generate_piece(black_piece, piece_coordinates, Color.black)
    ]

    board = Board(pieces)

    assert board.is_in_check(Color.white)

@pytest.mark.parametrize(
    "black_piece, piece_coordinates",
    [
        (PieceTypes.queen, 'A2'),
        (PieceTypes.queen, 'F3'),
        (PieceTypes.bishop, 'F8'),
        (PieceTypes.rook, 'E2'),
        (PieceTypes.knight, 'B2'),
        (PieceTypes.pawn, 'E1')
    ]
)
def test_is_in_check_returns_false_when_king_not_in_check(black_piece, piece_coordinates) -> None:
    pieces = [
        generate_piece(PieceTypes.king, 'D4', Color.white),
        generate_piece(black_piece, piece_coordinates, Color.black)
    ]

    board = Board(pieces)

    assert not board.is_in_check(Color.white)
