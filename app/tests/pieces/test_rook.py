import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import create_pieces, to_coordinates, get_possible_destinations


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
    rook = create_pieces(PieceType.Rook, "F4", Color.White)

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        rook, Board({rook})
    )

    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("B4", create_pieces(PieceType.Pawn, "B4", Color.White)),
        ("B4", create_pieces(PieceType.King, "C4", Color.White)),
        ("F6", create_pieces(PieceType.Rook, "F6", Color.White)),
        ("F6", create_pieces(PieceType.Rook, "F5", Color.Black)),
        ("H4", create_pieces(PieceType.Bishop, "H4", Color.White)),
        ("H4", create_pieces(PieceType.Queen, "G4", Color.Black)),
        ("F3", create_pieces(PieceType.Pawn, "F3", Color.White)),
        ("F1", create_pieces(PieceType.Pawn, "F2", Color.Black)),
    ],
)
def test_rook_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: MovablePiece
) -> None:
    rook = create_pieces(PieceType.Rook, "F4", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        rook, Board({rook, obstructing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("B4", create_pieces(PieceType.Pawn, "B4", Color.Black)),
        ("F6", create_pieces(PieceType.Rook, "F6", Color.Black)),
        ("H4", create_pieces(PieceType.Bishop, "H4", Color.Black)),
        ("F3", create_pieces(PieceType.Pawn, "F3", Color.Black)),
        ("F1", create_pieces(PieceType.Pawn, "F1", Color.Black)),
    ],
)
def test_rook_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: MovablePiece
) -> None:
    rook = create_pieces(PieceType.Rook, "F4", Color.White)

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        rook, Board({rook, opposing_piece})
    )
