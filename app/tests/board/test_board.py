import pytest
from chess import PieceType, Board, Color, Piece
from ..repository import create_pieces, create_move, to_coordinates


def test_try_get_piece_returns_piece_with_specified_coordinates() -> None:
    white_pawn = Piece(PieceType.Pawn, Color.White)
    coordinates = to_coordinates("A1")

    board = Board({
        coordinates: white_pawn
    })

    assert board.try_get_piece(coordinates) == white_pawn


def test_try_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    white_pawn = Piece(PieceType.Pawn, Color.White)

    board = Board({
        to_coordinates("A1"): white_pawn
    })

    assert board.try_get_piece(to_coordinates("B1")) == None


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
    board = Board({
        to_coordinates("D4"): Piece(PieceType.King, Color.White),
        to_coordinates(piece_coordinates): Piece(black_piece, Color.Black),
    })

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
        create_pieces(PieceType.King, "D4", Color.White),
        create_pieces(black_piece, piece_coordinates, Color.Black),
    }

    board = Board(pieces)

    assert not board.is_in_check(Color.White)


def test_move_via_en_passant_removes_piece() -> None:
    pawn = create_pieces(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_pieces(PieceType.Pawn, "G1", Color.Black)

    pieces = {pawn, enemy_pawn}

    board = Board(pieces)

    enemy_pawn_to_E1 = create_move((enemy_pawn, "E1"))
    board.move(enemy_pawn_to_E1)

    pawn_to_F1 = create_move((pawn, "F1"))
    board.move(pawn_to_F1)

    assert enemy_pawn not in board.pieces


def test_move_via_queenside_castle_moves_king_and_rook() -> None:
    king = create_pieces(PieceType.King, "A5", Color.White)
    rook = create_pieces(PieceType.Rook, "A1", Color.White)

    pieces = {king, rook}

    board = Board(pieces)

    king_to_A3 = create_move((king, "A3"))
    board.move(king_to_A3)

    assert king.coordinates == to_coordinates(
        "A3"
    ) and rook.coordinates == to_coordinates("A4")


def test_move_via_kingside_castle_moves_king_and_rook() -> None:
    king = create_pieces(PieceType.King, "A5", Color.White)
    rook = create_pieces(PieceType.Rook, "A8", Color.White)

    pieces = {king, rook}

    board = Board(pieces)

    king_to_A7 = create_move((king, "A7"))
    board.move(king_to_A7)

    assert king.coordinates == to_coordinates(
        "A7"
    ) and rook.coordinates == to_coordinates("A6")
