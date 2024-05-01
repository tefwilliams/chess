import pytest
from chess import PieceType, Board, Color
from ..repository import create_piece, create_move, to_coordinates


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    piece = create_piece(PieceType.Pawn, "A1", Color.White)
    get_from_coordinates = to_coordinates("A1")

    board = Board({piece})

    assert board.try_get_piece(get_from_coordinates) == piece


def test_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    piece = create_piece(PieceType.Pawn, "A1", Color.White)
    get_from_coordinates = to_coordinates("B1")

    board = Board({piece})

    assert board.try_get_piece(get_from_coordinates) == None


@pytest.mark.parametrize(
    "black_piece, piece_coordinates",
    [
        (PieceType.Queen, "A1"),
        (PieceType.Queen, "F4"),
        (PieceType.Bishop, "F2"),
        (PieceType.Rook, "D8"),
        (PieceType.Knight, "B3"),
        (PieceType.Pawn, "E5"),
    ],
)
def test_is_in_check_returns_true_when_king_in_check(
    black_piece, piece_coordinates
) -> None:
    pieces = {
        create_piece(PieceType.King, "D4", Color.White),
        create_piece(black_piece, piece_coordinates, Color.Black),
    }

    board = Board(pieces)

    assert board.is_in_check(Color.White)


@pytest.mark.parametrize(
    "black_piece, piece_coordinates",
    [
        (PieceType.Queen, "A2"),
        (PieceType.Queen, "F3"),
        (PieceType.Bishop, "F8"),
        (PieceType.Rook, "E2"),
        (PieceType.Knight, "B2"),
        (PieceType.Pawn, "E1"),
        (PieceType.Pawn, "E4"),
    ],
)
def test_is_in_check_returns_false_when_king_not_in_check(
    black_piece, piece_coordinates
) -> None:
    pieces = {
        create_piece(PieceType.King, "D4", Color.White),
        create_piece(black_piece, piece_coordinates, Color.Black),
    }

    board = Board(pieces)

    assert not board.is_in_check(Color.White)


def test_move_via_en_passant_removes_piece() -> None:
    pawn = create_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_piece(PieceType.Pawn, "G1", Color.Black)

    pieces = {pawn, enemy_pawn}

    board = Board(pieces)

    enemy_pawn_to_E1 = create_move((enemy_pawn, "E1"))
    board.move(enemy_pawn_to_E1)

    pawn_to_F1 = create_move((pawn, "F1"))
    board.move(pawn_to_F1)

    assert enemy_pawn not in board.pieces


def test_move_via_queenside_castle_moves_king_and_rook() -> None:
    king = create_piece(PieceType.King, "A5", Color.White)
    rook = create_piece(PieceType.Rook, "A1", Color.White)

    pieces = {king, rook}

    board = Board(pieces)

    king_to_A3 = create_move((king, "A3"))
    board.move(king_to_A3)

    assert king.coordinates == to_coordinates(
        "A3"
    ) and rook.coordinates == to_coordinates("A4")


def test_move_via_kingside_castle_moves_king_and_rook() -> None:
    king = create_piece(PieceType.King, "A5", Color.White)
    rook = create_piece(PieceType.Rook, "A8", Color.White)

    pieces = {king, rook}

    board = Board(pieces)

    king_to_A7 = create_move((king, "A7"))
    board.move(king_to_A7)

    assert king.coordinates == to_coordinates(
        "A7"
    ) and rook.coordinates == to_coordinates("A6")
