
from app.src import PieceTypes, Coordinates, Board, Color
from app.tests.board.data.generate_piece import generate_piece


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

def test_is_square_attacked_returns_true_when_piece_can_move_to_square() -> None:
    pieces = [
        generate_piece(PieceTypes.king, 'A4', Color.white),
        generate_piece(PieceTypes.king, 'G4', Color.black),
        generate_piece(PieceTypes.pawn, 'A1', Color.white),
        generate_piece(PieceTypes.pawn, 'B2', Color.black)
    ]

    square_coordinates = Coordinates.convert_from_grid_value('B2')
    opposing_color_to_piece = Color.get_opposing_color(Color.black)

    board = Board(pieces)

    assert board.is_square_attacked(square_coordinates, opposing_color_to_piece)
