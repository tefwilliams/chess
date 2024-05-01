import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import create_piece, to_coordinates


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

    board = Board([king])

    can_move = to_coordinates(square_to_move_to) in board.get_possible_moves(king)
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
    square_to_move_to: str, obstructing_piece: Piece
) -> None:
    king = create_piece(PieceType.King, "F4", Color.White)

    pieces = [king, obstructing_piece]

    board = Board(pieces)

    assert not to_coordinates(square_to_move_to) in board.get_possible_moves(king)


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
    square_to_move_to: str, opposing_piece: Piece
) -> None:
    king = create_piece(PieceType.King, "F4", Color.White)

    pieces = [king, opposing_piece]

    board = Board(pieces)

    assert to_coordinates(square_to_move_to) in board.get_possible_moves(king)


@pytest.mark.parametrize(
    "square_to_move_to, other_pieces, should_be_able_to_move",
    [
        ("A3", [], True),
        ("A7", [create_piece(PieceType.Rook, "E5", Color.Black)], False),
        ("A3", [create_piece(PieceType.Rook, "E5", Color.Black)], False),
        ("A7", [create_piece(PieceType.Rook, "E4", Color.Black)], True),
        ("A3", [create_piece(PieceType.Rook, "E4", Color.Black)], False),
        ("A2", [create_piece(PieceType.Rook, "E7", Color.Black)], False),
    ],
)
def test_king_can_move_via_castle(
    square_to_move_to: str, other_pieces: list[Piece], should_be_able_to_move: bool
) -> None:
    king = create_piece(PieceType.King, "A5", Color.White)

    rooks = [
        create_piece(PieceType.Rook, "A1", Color.White),
        create_piece(PieceType.Rook, "A8", Color.White),
    ]

    pieces = [king, *rooks, *other_pieces]

    board = Board(pieces)

    can_move = to_coordinates(square_to_move_to) in board.get_possible_moves(king)

    assert can_move == should_be_able_to_move


def test_king_cannot_move_via_castle_if_rook_has_moved() -> None:
    king = create_piece(PieceType.King, "A5", Color.White)

    rook = create_piece(PieceType.Rook, "A1", Color.White)

    pieces = [king, rook]

    board = Board(pieces)

    board.move(rook, to_coordinates("B1"))
    board.move(rook, to_coordinates("A1"))

    assert to_coordinates("A3") not in board.get_possible_moves(king)


def test_king_cannot_move_via_castle_if_king_has_moved() -> None:
    king = create_piece(PieceType.King, "A5", Color.White)

    rooks = [
        create_piece(PieceType.Rook, "A1", Color.White),
        create_piece(PieceType.Rook, "A8", Color.White),
    ]

    pieces = [king, *rooks]

    board = Board(pieces)

    board.move(king, to_coordinates("B5"))
    board.move(king, to_coordinates("A5"))

    assert all(
        to_coordinates(square) not in board.get_possible_moves(king)
        for square in ["A3", "A7"]
    )
