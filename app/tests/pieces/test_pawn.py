import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import create_piece, to_coordinates


def test_pawn_can_move_one_or_two_forward_if_it_has_not_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    assert (
        board.get_possible_moves(pawn).sort()
        == [
            to_coordinates("C2"),
            to_coordinates("B2"),
        ].sort()
    )


def test_pawn_can_move_two_forward_if_it_has_not_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    assert to_coordinates("C2") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_two_forward_if_it_has_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    board.move(pawn, to_coordinates("B2"))

    assert to_coordinates("D2") not in board.get_possible_moves(pawn)


def test_pawn_can_move_forward_diagonally_if_enemy_piece_there() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, create_piece(PieceType.Rook, "B1", Color.Black)]

    board = Board(pieces)

    assert to_coordinates("B1") in board.get_possible_moves(pawn)


def test_pawn_can_move_via_en_passant_if_enemy_pawn_has_just_moved_two_squares() -> (
    None
):
    pawn = create_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_piece(PieceType.Pawn, "G1", Color.Black)

    pieces = [pawn, enemy_pawn]

    board = Board(pieces)

    board.move(enemy_pawn, to_coordinates("E1"))

    assert to_coordinates("F1") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_via_en_passant_if_another_piece_has_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_piece(PieceType.Pawn, "G1", Color.Black)
    other_enempy_piece = create_piece(PieceType.Bishop, "H5", Color.Black)

    pieces = [pawn, enemy_pawn, other_enempy_piece]

    board = Board(pieces)

    board.move(enemy_pawn, to_coordinates("E1"))
    board.move(other_enempy_piece, to_coordinates("G4"))

    assert to_coordinates("F1") not in board.get_possible_moves(pawn)


def test_pawn_cannot_move_forward_diagonally_if_fiendly_piece_there() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, create_piece(PieceType.Rook, "B1", Color.White)]

    board = Board(pieces)

    assert to_coordinates("B1") not in board.get_possible_moves(pawn)


@pytest.mark.parametrize(
    "square_to_move_to, piece_at_destination",
    [
        ("C4", create_piece(PieceType.Queen, "C4", Color.Black)),
        ("C3", create_piece(PieceType.Rook, "C3", Color.Black)),
    ],
)
def test_pawn_cannot_move_two_forward_diagonally(
    square_to_move_to: str, piece_at_destination: Piece
) -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, piece_at_destination]

    board = Board(pieces)

    assert not to_coordinates(square_to_move_to) in board.get_possible_moves(pawn)


def test_pawn_cannot_move_backward() -> None:
    pawn = create_piece(PieceType.Pawn, "B1", Color.White)

    board = Board([pawn])

    assert not to_coordinates("A1") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_out_of_board() -> None:
    pawn = create_piece(PieceType.Pawn, "H2", Color.White)

    board = Board([pawn])

    assert len(board.get_possible_moves(pawn)) == 0
