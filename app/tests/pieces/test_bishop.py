import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import create_pieces, to_coordinates, get_possible_destinations


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("B4", False),
        ("E2", False),
        ("F6", False),
        ("C1", True),
        ("E5", True),
        ("G3", True),
    ],
)
def test_bishop_can_only_move_diagonally(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    bishop = create_pieces(PieceType.Bishop, "F4", Color.White)

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        bishop, Board({bishop})
    )

    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("C1", create_pieces(PieceType.Bishop, "C1", Color.White)),
        ("C1", create_pieces(PieceType.Queen, "E3", Color.Black)),
        ("E5", create_pieces(PieceType.Pawn, "E5", Color.White)),
        ("D6", create_pieces(PieceType.King, "E5", Color.White)),
        ("G3", create_pieces(PieceType.Rook, "G3", Color.White)),
        ("C7", create_pieces(PieceType.Knight, "C7", Color.White)),
    ],
)
def test_bishop_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: MovablePiece
) -> None:
    bishop = create_pieces(PieceType.Bishop, "F4", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        bishop, Board({bishop, obstructing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("C1", create_pieces(PieceType.Bishop, "C1", Color.Black)),
        ("E3", create_pieces(PieceType.Queen, "E3", Color.Black)),
        ("E5", create_pieces(PieceType.Pawn, "E5", Color.Black)),
        ("G3", create_pieces(PieceType.Rook, "G3", Color.Black)),
        ("C7", create_pieces(PieceType.Knight, "C7", Color.Black)),
    ],
)
def test_bishop_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: MovablePiece
) -> None:
    bishop = create_pieces(PieceType.Bishop, "F4", Color.White)

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        bishop, Board({bishop, opposing_piece})
    )
