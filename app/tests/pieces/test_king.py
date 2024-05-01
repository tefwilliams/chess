import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import (
    create_piece,
    to_coordinates,
    get_possible_destinations,
    create_move,
)


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("B1", False),
        ("B4", False),
        ("F6", False),
        ("F3", True),
        ("E5", True),
        ("G4", True),
        ("E4", True),
    ],
)
def test_king_can_only_move_to_adjacent_squares(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    king = create_piece(PieceType.King, "F4", Color.White)

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        king, Board({king})
    )

    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("F3", create_piece(PieceType.Bishop, "F3", Color.White)),
        ("E5", create_piece(PieceType.Rook, "E5", Color.White)),
        ("G4", create_piece(PieceType.Queen, "G4", Color.White)),
        ("E4", create_piece(PieceType.Pawn, "E4", Color.White)),
    ],
)
def test_king_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: MovablePiece
) -> None:
    king = create_piece(PieceType.King, "F4", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        king, Board({king, obstructing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("F3", create_piece(PieceType.Bishop, "F3", Color.Black)),
        ("E5", create_piece(PieceType.Rook, "E5", Color.Black)),
        ("G4", create_piece(PieceType.Queen, "G4", Color.Black)),
        ("E4", create_piece(PieceType.Pawn, "E4", Color.Black)),
    ],
)
def test_king_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: MovablePiece
) -> None:
    king = create_piece(PieceType.King, "F4", Color.White)

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        king, Board({king, opposing_piece})
    )


@pytest.mark.parametrize(
    "square_to_move_to, other_pieces, should_be_able_to_move",
    [
        ("C1", [], True),
        ("G1", [create_piece(PieceType.Rook, "E5", Color.Black)], False),
        ("C1", [create_piece(PieceType.Rook, "E5", Color.Black)], False),
        # TODO - this should still fail after fixing castle rules
        ("G1", [create_piece(PieceType.Rook, "E4", Color.Black)], True),
        ("C1", [create_piece(PieceType.Rook, "E4", Color.Black)], False),
        ("B1", [create_piece(PieceType.Rook, "E7", Color.Black)], False),
    ],
)
def test_king_can_move_via_castle(
    square_to_move_to: str,
    other_pieces: list[MovablePiece],
    should_be_able_to_move: bool,
) -> None:
    king = create_piece(PieceType.King, "E1", Color.White)

    rooks = [
        create_piece(PieceType.Rook, "A1", Color.White),
        create_piece(PieceType.Rook, "H1", Color.White),
    ]

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        king, Board({king, *rooks, *other_pieces})
    )

    assert can_move == should_be_able_to_move


def test_king_cannot_move_via_castle_if_rook_has_moved() -> None:
    king = create_piece(PieceType.King, "E1", Color.White)
    rook = create_piece(PieceType.Rook, "A1", Color.White)

    board = Board({king, rook})

    rook_to_A2 = create_move((rook, "A2"))
    board.move(rook_to_A2)

    rook_to_A1 = create_move((rook, "A1"))
    board.move(rook_to_A1)

    assert to_coordinates("A3") not in get_possible_destinations(king, board)


def test_king_cannot_move_via_castle_if_king_has_moved() -> None:
    king = create_piece(PieceType.King, "E1", Color.White)

    rooks = [
        create_piece(PieceType.Rook, "A1", Color.White),
        create_piece(PieceType.Rook, "H1", Color.White),
    ]

    board = Board({king, *rooks})

    king_to_E2 = create_move((king, "E2"))
    board.move(king_to_E2)

    king_to_E1 = create_move((king, "E1"))
    board.move(king_to_E1)

    assert all(
        to_coordinates(square) not in get_possible_destinations(king, board)
        for square in ["C1", "G1"]
    )
