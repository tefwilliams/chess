import pytest
from src import Color, PieceType, Piece
from ..repository import (
    create_board,
    get_possible_destinations,
    create_move,
)


@pytest.mark.parametrize(
    "color",
    [
        Color.White,
        Color.Black,
    ],
)
def test_king_can_only_move_to_adjacent_squares(color: Color) -> None:
    board = create_board(
        {
            "F4": Piece(PieceType.King, color),
        }
    )

    assert sorted(
        [
            "F5",
            "G5",
            "G4",
            "G3",
            "F3",
            "E3",
            "E4",
            "E5",
        ]
    ) == get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_pieces",
    [
        ("F3", {"F3": Piece(PieceType.Bishop, Color.White)}),
        ("E5", {"E5": Piece(PieceType.Rook, Color.White)}),
        ("G4", {"G4": Piece(PieceType.Queen, Color.White)}),
        ("E4", {"E4": Piece(PieceType.Pawn, Color.White)}),
    ],
)
def test_king_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_pieces: dict[str, Piece]
) -> None:

    board = create_board(
        {"F4": Piece(PieceType.King, Color.White), **obstructing_pieces}
    )

    assert not square_to_move_to in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_pieces",
    [
        ("F3", {"F3": Piece(PieceType.Bishop, Color.Black)}),
        ("E5", {"E5": Piece(PieceType.Rook, Color.Black)}),
        ("G4", {"G4": Piece(PieceType.Queen, Color.Black)}),
        ("E4", {"E4": Piece(PieceType.Pawn, Color.Black)}),
    ],
)
def test_king_can_take_opposing_piece(
    square_to_move_to: str, opposing_pieces: dict[str, Piece]
) -> None:
    board = create_board({"F4": Piece(PieceType.King, Color.White), **opposing_pieces})

    assert square_to_move_to in get_possible_destinations("F4", board)


@pytest.mark.parametrize(
    "square_to_move_to, other_pieces, should_be_able_to_move",
    [
        ("C1", {}, True),
        ("G1", {}, True),
        ("B1", {}, False),
        ("G1", {"E5": Piece(PieceType.Rook, Color.Black)}, False),
        ("C1", {"E5": Piece(PieceType.Rook, Color.Black)}, False),
        ("G1", {"F4": Piece(PieceType.Rook, Color.Black)}, False),
        ("C1", {"F4": Piece(PieceType.Rook, Color.Black)}, True),
        ("C1", {"E4": Piece(PieceType.Rook, Color.Black)}, False),
        ("C1", {"A7": Piece(PieceType.Rook, Color.Black)}, True),
        ("B1", {"E7": Piece(PieceType.Rook, Color.Black)}, False),
    ],
)
def test_king_can_move_via_castle(
    square_to_move_to: str,
    other_pieces: dict[str, Piece],
    should_be_able_to_move: bool,
) -> None:
    board = create_board(
        {
            "E1": Piece(PieceType.King, Color.White),
            "A1": Piece(PieceType.Rook, Color.White),
            "H1": Piece(PieceType.Rook, Color.White),
            **other_pieces,
        }
    )

    can_move = square_to_move_to in get_possible_destinations("E1", board)

    assert can_move == should_be_able_to_move


def test_king_cannot_move_via_castle_if_rook_has_moved() -> None:
    board = create_board(
        {
            "E1": Piece(PieceType.King, Color.White),
            "A1": Piece(PieceType.Rook, Color.White),
        }
    )

    rook_to_a2 = create_move("A1", "A2")
    board.move(rook_to_a2)

    rook_to_a1 = create_move("A2", "A1")
    board.move(rook_to_a1)

    assert "A3" not in get_possible_destinations("E1", board)


def test_king_cannot_move_via_castle_if_king_has_moved() -> None:
    board = create_board(
        {
            "E1": Piece(PieceType.King, Color.White),
            "A1": Piece(PieceType.Rook, Color.White),
            "H1": Piece(PieceType.Rook, Color.White),
        }
    )

    king_to_e2 = create_move("E1", "E2")
    board.move(king_to_e2)

    king_to_e1 = create_move("E2", "E1")
    board.move(king_to_e1)

    assert all(
        square not in get_possible_destinations("E1", board) for square in ["C1", "G1"]
    )
