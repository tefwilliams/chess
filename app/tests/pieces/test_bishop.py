
import pytest
from chess import Board, Color, PieceTypes, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ('A2', False),
        ('B4', False),
        ('E2', False),
        ('F6', False),
        ('C1', True),
        ('E5', True),
        ('G3', True)
    ]
)
def test_bishop_can_only_move_diagonally(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    bishop = generate_piece(PieceTypes.bishop, 'F4', Color.white)

    board = Board([bishop])

    can_move = get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(bishop)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ('C1', generate_piece(PieceTypes.bishop, 'C1', Color.white)),
        ('C1', generate_piece(PieceTypes.queen, 'E3', Color.black)),
        ('E5', generate_piece(PieceTypes.pawn, 'E5', Color.white)),
        ('D6', generate_piece(PieceTypes.king, 'E5', Color.white)),
        ('G3', generate_piece(PieceTypes.rook, 'G3', Color.white)),
        ('C7', generate_piece(PieceTypes.knight, 'C7', Color.white))
    ]
)
def test_bishop_cannot_move_if_obstructed(square_to_move_to: str, obstructing_piece: Piece) -> None:
    bishop = generate_piece(PieceTypes.bishop, 'F4', Color.white)

    pieces = [
        bishop,
        obstructing_piece
    ]

    board = Board(pieces)

    assert not get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(bishop)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ('C1', generate_piece(PieceTypes.bishop, 'C1', Color.black)),
        ('E3', generate_piece(PieceTypes.queen, 'E3', Color.black)),
        ('E5', generate_piece(PieceTypes.pawn, 'E5', Color.black)),
        ('G3', generate_piece(PieceTypes.rook, 'G3', Color.black)),
        ('C7', generate_piece(PieceTypes.knight, 'C7', Color.black))
    ]
)
def test_bishop_can_take_opposing_piece(square_to_move_to: str, opposing_piece: Piece) -> None:
    bishop = generate_piece(PieceTypes.bishop, 'F4', Color.white)

    pieces = [
        bishop,
        opposing_piece
    ]

    board = Board(pieces)

    assert get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(bishop)
