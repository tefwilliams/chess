
import pytest
from chess import PieceTypes, Board, Color, coordinates
from ..repository import generate_piece, get_coordinates_from_grid_value


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    piece = generate_piece(PieceTypes.pawn, 'A1', Color.white)
    get_from_coordinates = get_coordinates_from_grid_value('A1')

    board = Board([piece])

    assert board.get_piece(get_from_coordinates) == piece


def test_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    piece = generate_piece(PieceTypes.pawn, 'A1', Color.white)
    get_from_coordinates = get_coordinates_from_grid_value('B1')

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
        (PieceTypes.pawn, 'E1'),
        (PieceTypes.pawn, 'E4')
    ]
)
def test_is_in_check_returns_false_when_king_not_in_check(black_piece, piece_coordinates) -> None:
    pieces = [
        generate_piece(PieceTypes.king, 'D4', Color.white),
        generate_piece(black_piece, piece_coordinates, Color.black)
    ]

    board = Board(pieces)

    assert not board.is_in_check(Color.white)


def test_move_via_en_passant_removes_piece() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'E2', Color.white)
    enemy_pawn = generate_piece(PieceTypes.pawn, 'G1', Color.black)

    pieces = [
        pawn,
        enemy_pawn
    ]

    board = Board(pieces)

    board.evaluate_move(enemy_pawn, get_coordinates_from_grid_value('E1'))
    board.evaluate_move(pawn, get_coordinates_from_grid_value('F1'))

    assert enemy_pawn not in board.pieces


def test_move_via_queenside_castle_moves_king_and_rook() -> None:
    king = generate_piece(PieceTypes.king, 'A5', Color.white)
    rook = generate_piece(PieceTypes.rook, 'A1', Color.white)

    pieces = [
        king,
        rook
    ]

    board = Board(pieces)

    board.evaluate_move(king, get_coordinates_from_grid_value('A3'))

    assert (king.coordinates == get_coordinates_from_grid_value('A3')
            and rook.coordinates == get_coordinates_from_grid_value('A4'))


def test_move_via_kingside_castle_moves_king_and_rook() -> None:
    king = generate_piece(PieceTypes.king, 'A5', Color.white)
    rook = generate_piece(PieceTypes.rook, 'A8', Color.white)

    pieces = [
        king,
        rook
    ]

    board = Board(pieces)

    board.evaluate_move(king, get_coordinates_from_grid_value('A7'))

    assert (king.coordinates == get_coordinates_from_grid_value('A7')
            and rook.coordinates == get_coordinates_from_grid_value('A6'))
