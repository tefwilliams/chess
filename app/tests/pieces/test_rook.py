import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import create_piece, to_coordinates


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("E2", False),
        ("C1", False),
        ("H4", True),
        ("F3", True),
        ("B4", True),
        ("F6", True),
    ],
)
def test_rook_can_only_move_diagonally_or_orthogonally(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    rook = create_piece(PieceType.Rook, "F4", Color.White)

    board = Board([rook])

    can_move = to_coordinates(square_to_move_to) in board.get_possible_moves(rook)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("B4", create_piece(PieceType.Pawn, "B4", Color.White)),
        ("B4", create_piece(PieceType.King, "C4", Color.White)),
        ("F6", create_piece(PieceType.Rook, "F6", Color.White)),
        ("F6", create_piece(PieceType.Rook, "F5", Color.Black)),
        ("H4", create_piece(PieceType.Bishop, "H4", Color.White)),
        ("H4", create_piece(PieceType.Queen, "G4", Color.Black)),
        ("F3", create_piece(PieceType.Pawn, "F3", Color.White)),
        ("F1", create_piece(PieceType.Pawn, "F2", Color.Black)),
    ],
)
def test_rook_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: Piece
) -> None:
    rook = create_piece(PieceType.Rook, "F4", Color.White)

    pieces = [rook, obstructing_piece]

    board = Board(pieces)

    assert not to_coordinates(square_to_move_to) in board.get_possible_moves(rook)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("B4", create_piece(PieceType.Pawn, "B4", Color.Black)),
        ("F6", create_piece(PieceType.Rook, "F6", Color.Black)),
        ("H4", create_piece(PieceType.Bishop, "H4", Color.Black)),
        ("F3", create_piece(PieceType.Pawn, "F3", Color.Black)),
        ("F1", create_piece(PieceType.Pawn, "F1", Color.Black)),
    ],
)
def test_rook_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: Piece
) -> None:
    rook = create_piece(PieceType.Rook, "F4", Color.White)

    pieces = [rook, opposing_piece]

    board = Board(pieces)

    assert to_coordinates(square_to_move_to) in board.get_possible_moves(rook)
