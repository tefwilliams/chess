import pytest
from src import Color, PieceType, Piece
from ..repository import (
    create_board,
    get_possible_destinations,
    create_move,
)


def test_pawn_can_move_one_or_two_forward_if_it_has_not_moved() -> None:
    board = create_board({"A2": Piece(PieceType.Pawn, Color.White)})

    assert get_possible_destinations("A2", board) == sorted(
        [
            "A3",
            "A4",
        ]
    )


def test_pawn_can_only_move_one_forward_if_it_has_moved() -> None:
    board = create_board({"A2": Piece(PieceType.Pawn, Color.White)})

    pawn_to_a3 = create_move("A2", "A3")
    board.move(pawn_to_a3)

    assert get_possible_destinations("A3", board) == sorted(
        [
            "A4",
        ]
    )


def test_pawn_can_move_forward_diagonally_if_enemy_piece_there() -> None:
    board = create_board(
        {
            "A2": Piece(PieceType.Pawn, Color.White),
            "B3": Piece(PieceType.Rook, Color.Black),
        }
    )

    assert "B3" in get_possible_destinations("A2", board)


def test_pawn_can_move_via_en_passant_if_enemy_pawn_has_just_moved_two_squares() -> (
    None
):
    board = create_board(
        {
            "E5": Piece(PieceType.Pawn, Color.White),
            "F7": Piece(PieceType.Pawn, Color.Black),
        }
    )

    enemy_pawn_to_f5 = create_move("F7", "F5")
    board.move(enemy_pawn_to_f5)

    assert "F6" in get_possible_destinations("E5", board)


def test_pawn_cannot_move_via_en_passant_if_another_piece_has_moved() -> None:
    board = create_board(
        {
            "E5": Piece(PieceType.Pawn, Color.White),
            "F7": Piece(PieceType.Pawn, Color.Black),
            "H5": Piece(PieceType.Bishop, Color.Black),
        }
    )

    enemy_pawn_to_f5 = create_move("F7", "F5")
    board.move(enemy_pawn_to_f5)

    other_enemy_piece_to_g4 = create_move("H5", "G4")
    board.move(other_enemy_piece_to_g4)

    assert "F6" not in get_possible_destinations("E5", board)


def test_pawn_cannot_move_forward_diagonally_if_fiendly_piece_there() -> None:
    board = create_board(
        {
            "A2": Piece(PieceType.Pawn, Color.White),
            "B1": Piece(PieceType.Rook, Color.White),
        }
    )

    assert "B1" not in get_possible_destinations("A2", board)


@pytest.mark.parametrize(
    "square_to_move_to, piece_at_destination",
    [
        ("C4", {"C4": Piece(PieceType.Queen, Color.Black)}),
        ("B4", {"C3": Piece(PieceType.Rook, Color.Black)}),
    ],
)
def test_pawn_cannot_move_two_forward_diagonally(
    square_to_move_to: str, piece_at_destination: dict[str, Piece]
) -> None:
    board = create_board(
        {"A2": Piece(PieceType.Pawn, Color.White), **piece_at_destination}
    )

    assert not square_to_move_to in get_possible_destinations("A2", board)


def test_pawn_cannot_move_backward() -> None:
    board = create_board({"A2": Piece(PieceType.Pawn, Color.White)})

    assert not "A1" in get_possible_destinations("A2", board)


def test_pawn_cannot_move_out_of_board() -> None:
    board = create_board({"A8": Piece(PieceType.Pawn, Color.White)})

    assert get_possible_destinations("A8", board) == []
