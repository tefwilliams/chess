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
def test_queen_can_only_move_diagonally_or_orthogonally(color: Color) -> None:
    board = create_board({"F4": Piece(PieceType.Queen, color)})

    assert sorted(
        [
            "B8",
            "C7",
            "D6",
            "E5",
            "G3",
            "H2",
            "C1",
            "F8",
            "F7",
            "F6",
            "F5",
            "F3",
            "F2",
            "F1",
            "D2",
            "E3",
            "G5",
            "H6",
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
        ("F6", {"F5": Piece(PieceType.Rook, Color.Black)}),
        ("C1", {"C1": Piece(PieceType.Bishop, Color.White)}),
        ("C1", {"E3": Piece(PieceType.Queen, Color.Black)}),
        ("E5", {"E5": Piece(PieceType.Pawn, Color.White)}),
        ("D6", {"E5": Piece(PieceType.King, Color.White)}),
        ("G3", {"G3": Piece(PieceType.Rook, Color.White)}),
        ("C7", {"C7": Piece(PieceType.Knight, Color.White)}),
    ],
)
def test_queen_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_pieces: dict[str, Piece]
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Queen, Color.White), **obstructing_pieces}
    )

    assert not square_to_move_to in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_pieces",
    [
        ("B4", {"B4": Piece(PieceType.Pawn, Color.Black)}),
        ("F6", {"F6": Piece(PieceType.Rook, Color.Black)}),
        ("C1", {"C1": Piece(PieceType.Bishop, Color.Black)}),
        ("E3", {"E3": Piece(PieceType.Queen, Color.Black)}),
        ("E5", {"E5": Piece(PieceType.Pawn, Color.Black)}),
        ("G3", {"G3": Piece(PieceType.Rook, Color.Black)}),
        ("C7", {"C7": Piece(PieceType.Knight, Color.Black)}),
    ],
)
def test_queen_can_take_opposing_piece(
    square_to_move_to: str, opposing_pieces: dict[str, Piece]
) -> None:
    board = create_board({"F4": Piece(PieceType.Queen, Color.White), **opposing_pieces})

    assert square_to_move_to in get_possible_destinations("F4", board)
