import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


def test_pawn_can_move_one_or_two_forward_if_it_has_not_moved() -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    assert (
        board.get_possible_moves(pawn).sort()
        == [
            get_coordinates_from_grid_value("C2"),
            get_coordinates_from_grid_value("B2"),
        ].sort()
    )


def test_pawn_can_move_two_forward_if_it_has_not_moved() -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    assert get_coordinates_from_grid_value("C2") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_two_forward_if_it_has_moved() -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    board = Board([pawn])

    board.move(pawn, get_coordinates_from_grid_value("B2"))

    assert get_coordinates_from_grid_value("D2") not in board.get_possible_moves(pawn)


def test_pawn_can_move_forward_diagonally_if_enemy_piece_there() -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, generate_piece(PieceType.Rook, "B1", Color.Black)]

    board = Board(pieces)

    assert get_coordinates_from_grid_value("B1") in board.get_possible_moves(pawn)


def test_pawn_can_move_via_en_passant_if_enemy_pawn_has_just_moved_two_squares() -> (
    None
):
    pawn = generate_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = generate_piece(PieceType.Pawn, "G1", Color.Black)

    pieces = [pawn, enemy_pawn]

    board = Board(pieces)

    board.move(enemy_pawn, get_coordinates_from_grid_value("E1"))

    assert get_coordinates_from_grid_value("F1") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_via_en_passant_if_another_piece_has_moved() -> None:
    pawn = generate_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = generate_piece(PieceType.Pawn, "G1", Color.Black)
    other_enempy_piece = generate_piece(PieceType.Bishop, "H5", Color.Black)

    pieces = [pawn, enemy_pawn, other_enempy_piece]

    board = Board(pieces)

    board.move(enemy_pawn, get_coordinates_from_grid_value("E1"))
    board.move(other_enempy_piece, get_coordinates_from_grid_value("G4"))

    assert get_coordinates_from_grid_value("F1") not in board.get_possible_moves(pawn)


def test_pawn_cannot_move_forward_diagonally_if_fiendly_piece_there() -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, generate_piece(PieceType.Rook, "B1", Color.White)]

    board = Board(pieces)

    assert get_coordinates_from_grid_value("B1") not in board.get_possible_moves(pawn)


@pytest.mark.parametrize(
    "square_to_move_to, piece_at_destination",
    [
        ("C4", generate_piece(PieceType.Queen, "C4", Color.Black)),
        ("C3", generate_piece(PieceType.Rook, "C3", Color.Black)),
    ],
)
def test_pawn_cannot_move_two_forward_diagonally(
    square_to_move_to: str, piece_at_destination: Piece
) -> None:
    pawn = generate_piece(PieceType.Pawn, "A2", Color.White)

    pieces = [pawn, piece_at_destination]

    board = Board(pieces)

    assert not get_coordinates_from_grid_value(
        square_to_move_to
    ) in board.get_possible_moves(pawn)


def test_pawn_cannot_move_backward() -> None:
    pawn = generate_piece(PieceType.Pawn, "B1", Color.White)

    board = Board([pawn])

    assert not get_coordinates_from_grid_value("A1") in board.get_possible_moves(pawn)


def test_pawn_cannot_move_out_of_board() -> None:
    pawn = generate_piece(PieceType.Pawn, "H2", Color.White)

    board = Board([pawn])

    assert len(board.get_possible_moves(pawn)) == 0
