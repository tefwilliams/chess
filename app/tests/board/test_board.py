import pytest
from chess import PieceType, Board, Color, coordinates
from ..repository import generate_piece, get_coordinates_from_grid_value


def test_get_piece_returns_piece_with_specified_coordinates() -> None:
    piece = generate_piece(PieceType.Pawn, "A1", Color.White)
    get_from_coordinates = get_coordinates_from_grid_value("A1")

    board = Board([piece])

    assert board.try_get_piece(get_from_coordinates) == piece


def test_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    piece = generate_piece(PieceType.Pawn, "A1", Color.White)
    get_from_coordinates = get_coordinates_from_grid_value("B1")

    board = Board([piece])

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
    pieces = [
        generate_piece(PieceType.King, "D4", Color.White),
        generate_piece(black_piece, piece_coordinates, Color.Black),
    ]

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
    pieces = [
        generate_piece(PieceType.King, "D4", Color.White),
        generate_piece(black_piece, piece_coordinates, Color.Black),
    ]

    board = Board(pieces)

    assert not board.is_in_check(Color.White)


def test_move_via_en_passant_removes_piece() -> None:
    pawn = generate_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = generate_piece(PieceType.Pawn, "G1", Color.Black)

    pieces = [pawn, enemy_pawn]

    board = Board(pieces)

    board.move(enemy_pawn, get_coordinates_from_grid_value("E1"))
    board.move(pawn, get_coordinates_from_grid_value("F1"))

    assert enemy_pawn not in board.pieces


def test_move_via_queenside_castle_moves_king_and_rook() -> None:
    king = generate_piece(PieceType.King, "A5", Color.White)
    rook = generate_piece(PieceType.Rook, "A1", Color.White)

    pieces = [king, rook]

    board = Board(pieces)

    board.move(king, get_coordinates_from_grid_value("A3"))

    assert king.coordinates == get_coordinates_from_grid_value(
        "A3"
    ) and rook.coordinates == get_coordinates_from_grid_value("A4")


def test_move_via_kingside_castle_moves_king_and_rook() -> None:
    king = generate_piece(PieceType.King, "A5", Color.White)
    rook = generate_piece(PieceType.Rook, "A8", Color.White)

    pieces = [king, rook]

    board = Board(pieces)

    board.move(king, get_coordinates_from_grid_value("A7"))

    assert king.coordinates == get_coordinates_from_grid_value(
        "A7"
    ) and rook.coordinates == get_coordinates_from_grid_value("A6")
