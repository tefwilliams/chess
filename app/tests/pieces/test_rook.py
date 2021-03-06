
import pytest
from chess import Board, Color, PieceTypes, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ('A2', False),
        ('E2', False),
        ('C1', False),
        ('H4', True),
        ('F3', True),
        ('B4', True),
        ('F6', True),
    ]
)
def test_rook_can_only_move_diagonally_or_orthogonally(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    rook = generate_piece(PieceTypes.rook, 'F4', Color.white)

    board = Board([rook])

    can_move = get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(rook)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ('B4', generate_piece(PieceTypes.pawn, 'B4', Color.white)),
        ('B4', generate_piece(PieceTypes.king, 'C4', Color.white)),
        ('F6', generate_piece(PieceTypes.rook, 'F6', Color.white)),
        ('F6', generate_piece(PieceTypes.rook, 'F5', Color.black)),
        ('H4', generate_piece(PieceTypes.bishop, 'H4', Color.white)),
        ('H4', generate_piece(PieceTypes.queen, 'G4', Color.black)),
        ('F3', generate_piece(PieceTypes.pawn, 'F3', Color.white)),
        ('F1', generate_piece(PieceTypes.pawn, 'F2', Color.black))
    ]
)
def test_rook_cannot_move_if_obstructed(square_to_move_to: str, obstructing_piece: Piece) -> None:
    rook = generate_piece(PieceTypes.rook, 'F4', Color.white)

    pieces = [
        rook,
        obstructing_piece
    ]

    board = Board(pieces)

    assert not get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(rook)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ('B4', generate_piece(PieceTypes.pawn, 'B4', Color.black)),
        ('F6', generate_piece(PieceTypes.rook, 'F6', Color.black)),
        ('H4', generate_piece(PieceTypes.bishop, 'H4', Color.black)),
        ('F3', generate_piece(PieceTypes.pawn, 'F3', Color.black)),
        ('F1', generate_piece(PieceTypes.pawn, 'F1', Color.black))
    ]
)
def test_rook_can_take_opposing_piece(square_to_move_to: str, opposing_piece: Piece) -> None:
    rook = generate_piece(PieceTypes.rook, 'F4', Color.white)

    pieces = [
        rook,
        opposing_piece
    ]

    board = Board(pieces)

    assert get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(rook)
