import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import create_piece, to_coordinates, get_possible_destinations


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("E2", False),
        ("B4", True),
        ("F6", True),
        ("C1", True),
        ("E5", True),
        ("G3", True),
    ],
)
def test_queen_can_only_move_diagonally_or_orthogonally(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    queen = create_piece(PieceType.Queen, "F4", Color.White)

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        queen, Board({queen})
    )

    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("B4", create_piece(PieceType.Pawn, "B4", Color.White)),
        ("F6", create_piece(PieceType.Rook, "F5", Color.Black)),
        ("C1", create_piece(PieceType.Bishop, "C1", Color.White)),
        ("C1", create_piece(PieceType.Queen, "E3", Color.Black)),
        ("E5", create_piece(PieceType.Pawn, "E5", Color.White)),
        ("D6", create_piece(PieceType.King, "E5", Color.White)),
        ("G3", create_piece(PieceType.Rook, "G3", Color.White)),
        ("C7", create_piece(PieceType.Knight, "C7", Color.White)),
    ],
)
def test_queen_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: MovablePiece
) -> None:
    queen = create_piece(PieceType.Queen, "F4", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        queen, Board({queen, obstructing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("B4", create_piece(PieceType.Pawn, "B4", Color.Black)),
        ("F6", create_piece(PieceType.Rook, "F6", Color.Black)),
        ("C1", create_piece(PieceType.Bishop, "C1", Color.Black)),
        ("E3", create_piece(PieceType.Queen, "E3", Color.Black)),
        ("E5", create_piece(PieceType.Pawn, "E5", Color.Black)),
        ("G3", create_piece(PieceType.Rook, "G3", Color.Black)),
        ("C7", create_piece(PieceType.Knight, "C7", Color.Black)),
    ],
)
def test_queen_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: MovablePiece
) -> None:
    queen = create_piece(PieceType.Queen, "F4", Color.White)

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        queen, Board({queen, opposing_piece})
    )
