
from app.src import Board, Coordinates, Color, PieceTypes
from app.tests.data.generate_piece import generate_piece


def test_bishop_can_move_diagonally_if_no_piece_there() -> None:
    bishop = generate_piece(PieceTypes.bishop, 'A1', Color.white)

    board = Board([bishop])

    assert Coordinates.convert_from_grid_value('E5') in bishop.get_possible_moves(board)

def test_bishop_cannot_move_if_obstructed() -> None:
    bishop = generate_piece(PieceTypes.bishop, 'A1', Color.white)

    pieces = [
        bishop,
        generate_piece(PieceTypes.bishop, 'B2', Color.white)
    ]

    board = Board(pieces)

    assert not Coordinates.convert_from_grid_value('E5') in bishop.get_possible_moves(board)

def test_bishop_can_take_opposing_piece() -> None:
    bishop = generate_piece(PieceTypes.bishop, 'A1', Color.white)

    pieces = [
        bishop,
        generate_piece(PieceTypes.bishop, 'C3', Color.black)
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value('C3') in bishop.get_possible_moves(board)
