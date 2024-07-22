import pytest
from chess import PieceType, Board, Color, Piece
from ..repository import create_move, create_en_passant_move, to_coordinates


def test_try_get_piece_returns_piece_with_specified_coordinates() -> None:
    white_pawn = Piece(PieceType.Pawn, Color.White)
    coordinates = to_coordinates("A1")

    board = Board({coordinates: white_pawn})

    assert board.try_get_piece(coordinates) == white_pawn


def test_try_get_piece_returns_none_if_no_piece_has_specified_coordinates() -> None:
    white_pawn = Piece(PieceType.Pawn, Color.White)

    board = Board({to_coordinates("A1"): white_pawn})

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
    board = Board(
        {
            to_coordinates("D4"): Piece(PieceType.King, Color.White),
            to_coordinates(piece_coordinates): Piece(black_piece, Color.Black),
        }
    )

    assert board.in_check(Color.White)


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
    board = Board(
        {
            to_coordinates("D4"): Piece(PieceType.King, Color.White),
            to_coordinates(piece_coordinates): Piece(black_piece, Color.Black),
        }
    )

    assert not board.in_check(Color.White)


def test_move_via_en_passant_removes_piece() -> None:
    pawn = Piece(PieceType.Pawn, Color.White)
    enemy_pawn = Piece(PieceType.Pawn, Color.Black)

    board = Board({to_coordinates("E2"): pawn, to_coordinates("G1"): enemy_pawn})

    enemy_pawn_to_e1 = create_move("G1", "E1")
    board.move(enemy_pawn_to_e1)

    assert board.get_piece(to_coordinates("E1")) == enemy_pawn

    pawn_to_f1 = create_en_passant_move("E2", "F1", "E1")
    board.move(pawn_to_f1)

    assert board.try_get_piece(to_coordinates("E1")) is None


def test_move_via_queenside_castle_moves_king_and_rook() -> None:
    king = Piece(PieceType.King, Color.White)
    rook = Piece(PieceType.Rook, Color.White)

    board = Board({to_coordinates("A5"): king, to_coordinates("A1"): rook})

    king_to_a3 = create_move("A5", "A3")
    board.move(king_to_a3)

    assert (
        board.get_piece(to_coordinates("A3")) == king
        and board.get_piece(to_coordinates("A4")) == rook
    )


def test_move_via_kingside_castle_moves_king_and_rook() -> None:
    king = Piece(PieceType.King, Color.White)
    rook = Piece(PieceType.Rook, Color.White)

    board = Board({to_coordinates("A5"): king, to_coordinates("A8"): rook})

    king_to_a7 = create_move((king, "A7"))
    board.move(king_to_a7)

    assert (
        board.get_piece(to_coordinates("A7")) == king
        and board.get_piece(to_coordinates("A6")) == rook
    )
