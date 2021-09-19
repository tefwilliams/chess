
import pytest
from chess import Board, Color, PieceTypes, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ('A2', False),
        ('B1', False),
        ('B4', False),
        ('F6', False),
        ('B2', False),
        ('F5', False),
        ('E4', False),
        ('H3', True),
        ('E6', True),
        ('D3', True),
        ('G2', True)
    ]
)
def test_knight_can_only_move_to_knight_squares(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    knight = generate_piece(PieceTypes.knight, 'F4', Color.white)

    board = Board([knight])

    can_move = get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(knight)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ('H3', generate_piece(PieceTypes.bishop, 'H3', Color.white)),
        ('E6', generate_piece(PieceTypes.rook, 'E6', Color.white)),
        ('D3', generate_piece(PieceTypes.queen, 'D3', Color.white)),
        ('G2', generate_piece(PieceTypes.pawn, 'G2', Color.white))
    ]
)
def test_knight_cannot_move_if_obstructed(square_to_move_to: str, obstructing_piece: Piece) -> None:
    knight = generate_piece(PieceTypes.knight, 'F4', Color.white)

    pieces = [
        knight,
        obstructing_piece
    ]

    board = Board(pieces)

    assert not get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(knight)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ('H3', generate_piece(PieceTypes.bishop, 'H3', Color.black)),
        ('E6', generate_piece(PieceTypes.rook, 'E6', Color.black)),
        ('D3', generate_piece(PieceTypes.queen, 'D3', Color.black)),
        ('G2', generate_piece(PieceTypes.pawn, 'G2', Color.black))
    ]
)
def test_knight_can_take_opposing_piece(square_to_move_to: str, opposing_piece: Piece) -> None:
    knight = generate_piece(PieceTypes.knight, 'F4', Color.white)

    pieces = [
        knight,
        opposing_piece
    ]

    board = Board(pieces)

    assert get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(knight)
