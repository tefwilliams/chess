import pytest
from src import Color, PieceType, Piece
from ..repository import create_board, get_possible_destinations


@pytest.mark.parametrize(
    "color",
    [
        Color.White,
        Color.Black,
    ],
)
def test_rook_can_only_move_orthogonally(color: Color) -> None:
    board = create_board({"F4": Piece(PieceType.Rook, color)})

    assert sorted(
        [
            "F8",
            "F7",
            "F6",
            "F5",
            "F3",
            "F2",
            "F1",
            "A4",
            "B4",
            "C4",
            "D4",
            "E4",
            "G4",
            "H4",
        ]
    ) == get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_pieces",
    [
        ("B4", {"B4": Piece(PieceType.Pawn, Color.White)}),
        ("B4", {"C4": Piece(PieceType.King, Color.White)}),
        ("F6", {"F6": Piece(PieceType.Rook, Color.White)}),
        ("F6", {"F5": Piece(PieceType.Rook, Color.Black)}),
        ("H4", {"H4": Piece(PieceType.Bishop, Color.White)}),
        ("H4", {"G4": Piece(PieceType.Queen, Color.Black)}),
        ("F3", {"F3": Piece(PieceType.Pawn, Color.White)}),
        ("F1", {"F2": Piece(PieceType.Pawn, Color.Black)}),
    ],
)
def test_rook_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_pieces: dict[str, Piece]
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Rook, Color.White), **obstructing_pieces}
    )

    assert not square_to_move_to in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_pieces",
    [
        ("B4", {"B4": Piece(PieceType.Pawn, Color.Black)}),
        ("F6", {"F6": Piece(PieceType.Rook, Color.Black)}),
        ("H4", {"H4": Piece(PieceType.Bishop, Color.Black)}),
        ("F3", {"F3": Piece(PieceType.Pawn, Color.Black)}),
        ("F1", {"F1": Piece(PieceType.Pawn, Color.Black)}),
    ],
)
def test_rook_can_take_opposing_piece(
    square_to_move_to: str, opposing_pieces: dict[str, Piece]
) -> None:
    board = create_board({"F4": Piece(PieceType.Rook, Color.White), **opposing_pieces})

    assert square_to_move_to in get_possible_destinations("F4", board)
