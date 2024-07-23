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
def test_knight_can_only_move_to_knight_squares(color: Color) -> None:
    board = create_board({"F4": Piece(PieceType.Knight, color)})

    assert sorted(
        [
            "E6",
            "G6",
            "H5",
            "H3",
            "G2",
            "E2",
            "D3",
            "D5",
        ]
    ) == get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_pieces",
    [
        ("H3", {"H3": Piece(PieceType.Bishop, Color.White)}),
        ("E6", {"E6": Piece(PieceType.Rook, Color.White)}),
        ("D3", {"D3": Piece(PieceType.Queen, Color.White)}),
        ("G2", {"G2": Piece(PieceType.Pawn, Color.White)}),
    ],
)
def test_knight_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_pieces: dict[str, Piece]
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Knight, Color.White), **obstructing_pieces}
    )

    assert not square_to_move_to in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_pieces",
    [
        ("H3", {"H3": Piece(PieceType.Bishop, Color.Black)}),
        ("E6", {"E6": Piece(PieceType.Rook, Color.Black)}),
        ("D3", {"D3": Piece(PieceType.Queen, Color.Black)}),
        ("G2", {"G2": Piece(PieceType.Pawn, Color.Black)}),
    ],
)
def test_knight_can_take_opposing_piece(
    square_to_move_to: str, opposing_pieces: Piece
) -> None:
    board = create_board(
        {"F4": Piece(PieceType.Knight, Color.White), **opposing_pieces}
    )

    assert square_to_move_to in get_possible_destinations("F4", board)
