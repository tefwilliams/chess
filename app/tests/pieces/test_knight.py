import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import create_piece, to_coordinates, get_possible_destinations


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("B1", False),
        ("B4", False),
        ("F6", False),
        ("B2", False),
        ("F5", False),
        ("E4", False),
        ("H3", True),
        ("E6", True),
        ("D3", True),
        ("G2", True),
    ],
)
def test_knight_can_only_move_to_knight_squares(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    knight = create_piece(PieceType.Knight, "F4", Color.White)

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        knight, Board({knight})
    )

    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("H3", create_piece(PieceType.Bishop, "H3", Color.White)),
        ("E6", create_piece(PieceType.Rook, "E6", Color.White)),
        ("D3", create_piece(PieceType.Queen, "D3", Color.White)),
        ("G2", create_piece(PieceType.Pawn, "G2", Color.White)),
    ],
)
def test_knight_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: MovablePiece
) -> None:
    knight = create_piece(PieceType.Knight, "F4", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        knight, Board({knight, obstructing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("H3", create_piece(PieceType.Bishop, "H3", Color.Black)),
        ("E6", create_piece(PieceType.Rook, "E6", Color.Black)),
        ("D3", create_piece(PieceType.Queen, "D3", Color.Black)),
        ("G2", create_piece(PieceType.Pawn, "G2", Color.Black)),
    ],
)
def test_knight_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: MovablePiece
) -> None:
    knight = create_piece(PieceType.Knight, "F4", Color.White)

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        knight, Board({knight, opposing_piece})
    )
