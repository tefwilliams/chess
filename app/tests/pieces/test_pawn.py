import pytest
from chess import Board, Color, PieceType, MovablePiece
from ..repository import (
    create_piece,
    to_coordinates,
    get_possible_destinations,
    create_move,
)


def test_pawn_can_move_one_or_two_forward_if_it_has_not_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    assert get_possible_destinations(pawn, Board({pawn})) == {
        to_coordinates("A3"),
        to_coordinates("A4"),
    }


def test_pawn_can_only_move_one_forward_if_it_has_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    board = Board({pawn})

    pawn_to_A3 = create_move((pawn, "A3"))
    board.move(pawn_to_A3)

    assert get_possible_destinations(pawn, Board({pawn})) == {
        to_coordinates("A4"),
    }


def test_pawn_can_move_forward_diagonally_if_enemy_piece_there() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    assert to_coordinates("B3") in get_possible_destinations(
        pawn, Board({pawn, create_piece(PieceType.Rook, "B3", Color.Black)})
    )


def test_pawn_can_move_via_en_passant_if_enemy_pawn_has_just_moved_two_squares() -> (
    None
):
    pawn = create_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_piece(PieceType.Pawn, "G1", Color.Black)

    board = Board({pawn, enemy_pawn})

    pawn_to_E1 = create_move((pawn, "E1"))
    board.move(pawn_to_E1)

    assert to_coordinates("F1") in get_possible_destinations(pawn, board)


def test_pawn_cannot_move_via_en_passant_if_another_piece_has_moved() -> None:
    pawn = create_piece(PieceType.Pawn, "E2", Color.White)
    enemy_pawn = create_piece(PieceType.Pawn, "G1", Color.Black)
    other_enempy_piece = create_piece(PieceType.Bishop, "H5", Color.Black)

    board = Board({pawn, enemy_pawn, other_enempy_piece})

    enemy_pawn_to_E1 = create_move((enemy_pawn, "E1"))
    board.move(enemy_pawn_to_E1)

    other_enemy_piece_to_G4 = create_move((other_enempy_piece, "G4"))
    board.move(other_enemy_piece_to_G4)

    assert to_coordinates("F1") not in get_possible_destinations(pawn, board)


def test_pawn_cannot_move_forward_diagonally_if_fiendly_piece_there() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    assert to_coordinates("B1") not in get_possible_destinations(
        pawn, Board({pawn, create_piece(PieceType.Rook, "B1", Color.White)})
    )


@pytest.mark.parametrize(
    "square_to_move_to, piece_at_destination",
    [
        ("C4", create_piece(PieceType.Queen, "C4", Color.Black)),
        ("B4", create_piece(PieceType.Rook, "C3", Color.Black)),
    ],
)
def test_pawn_cannot_move_two_forward_diagonally(
    square_to_move_to: str, piece_at_destination: MovablePiece
) -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        pawn, Board({pawn, piece_at_destination})
    )


def test_pawn_cannot_move_backward() -> None:
    pawn = create_piece(PieceType.Pawn, "A2", Color.White)

    assert not to_coordinates("A1") in get_possible_destinations(pawn, Board({pawn}))


def test_pawn_cannot_move_out_of_board() -> None:
    pawn = create_piece(PieceType.Pawn, "A8", Color.White)

    assert len(get_possible_destinations(pawn, Board({pawn}))) == 0
