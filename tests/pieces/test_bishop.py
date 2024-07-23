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
def test_bishop_can_only_move_diagonally(color: Color) -> None:
    board = create_board(
        {
            "F4": Piece(PieceType.Bishop, color),
        }
    )

    assert sorted(
        [
            "B8",
            "C7",
            "D6",
            "E5",
            "G3",
            "H2",
            "C1",
            "D2",
            "E3",
            "G5",
            "H6",
        ]
    ) == get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "destination, obstructing_pieces",
    [
        ("C1", {"C1": Piece(PieceType.Bishop, Color.White)}),
        ("C1", {"E3": Piece(PieceType.Queen, Color.Black)}),
        ("E5", {"E5": Piece(PieceType.Pawn, Color.White)}),
        ("D6", {"E5": Piece(PieceType.King, Color.White)}),
        ("G3", {"G3": Piece(PieceType.Rook, Color.White)}),
        ("C7", {"C7": Piece(PieceType.Knight, Color.White)}),
    ],
)
def test_bishop_cannot_move_if_obstructed(
    destination: str, obstructing_pieces: dict[str, Piece]
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Bishop, Color.White), **obstructing_pieces}
    )

    assert not destination in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "destination, opposing_pieces",
    [
        ("C1", {"C1": Piece(PieceType.Bishop, Color.White)}),
        ("C1", {"E3": Piece(PieceType.Queen, Color.Black)}),
        ("E5", {"E5": Piece(PieceType.Pawn, Color.White)}),
        ("D6", {"E5": Piece(PieceType.King, Color.White)}),
        ("G3", {"G3": Piece(PieceType.Rook, Color.White)}),
        ("C7", {"C7": Piece(PieceType.Knight, Color.White)}),
    ],
)
def test_bishop_can_take_opposing_piece(
    destination: str, opposing_pieces: dict[str, Piece]
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Bishop, Color.White), **opposing_pieces}
    )

    assert not destination in get_possible_destinations("F4", board)
