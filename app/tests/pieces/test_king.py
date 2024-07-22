import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import (
    create_pieces,
    to_coordinates,
    get_possible_destinations,
    create_move,
)


@pytest.mark.parametrize(
    "color",
    [
        Color.White,
        Color.Black,
    ],
)
def test_king_can_only_move_to_adjacent_squares(color: Color) -> None:
    king_location = to_coordinates("F4")

    board = Board({
        king_location: Piece(PieceType.King, color),
    })

    assert {
        to_coordinates("F5"),
        to_coordinates("G5"),
        to_coordinates("G4"),
        to_coordinates("G3"),
        to_coordinates("F3"),
        to_coordinates("E3"),
        to_coordinates("E4"),
        to_coordinates("E5"),
    } == get_possible_destinations(king_location, board)


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece, obstructing_piece_location",
    [
        ("F3", Piece(PieceType.Bishop, Color.White), "F3"),
        ("E5", Piece(PieceType.Rook, Color.White), "E5"),
        ("G4", Piece(PieceType.Queen, Color.White), "G4"),
        ("E4", Piece(PieceType.Pawn, Color.White), "E4"),
    ],
)
def test_king_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: Piece, obstructing_piece_location: str
) -> None:
    king_location = to_coordinates("F4")

    board = Board({
        king_location: Piece(PieceType.King, Color.White),
        to_coordinates(obstructing_piece_location): obstructing_piece
    })

    assert not to_coordinates(square_to_move_to) in get_possible_destinations(
        king_location, board
    )


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece, opposing_piece_location",
    [
        ("F3", Piece(PieceType.Bishop, Color.Black), "F3"),
        ("E5", Piece(PieceType.Rook, Color.Black), "E5"),
        ("G4", Piece(PieceType.Queen, Color.Black), "G4"),
        ("E4", Piece(PieceType.Pawn, Color.Black), "E4"),
    ],
)
def test_king_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: Piece, opposing_piece_location: str
) -> None:
    king_location = to_coordinates("F4")

    # TODO - create board wrapper so we can use string coords
    board = Board({
        king_location: Piece(PieceType.King, Color.White),
        to_coordinates(opposing_piece_location): opposing_piece
    })

    assert to_coordinates(square_to_move_to) in get_possible_destinations(
        king_location, board
    )


@pytest.mark.parametrize(
    "square_to_move_to, other_pieces, should_be_able_to_move",
    [
        ("C1", [], True),
        ("G1", [(Piece(PieceType.Rook, Color.Black), "E5")], False),
        ("C1", [(Piece(PieceType.Rook, Color.Black), "E5")], False),
        # TODO - this should still fail after fixing castle rules
        ("G1", [(Piece(PieceType.Rook, Color.Black), "E4")], True),
        ("C1", [(Piece(PieceType.Rook, Color.Black), "E4")], False),
        ("B1", [(Piece(PieceType.Rook, Color.Black), "E7")], False),
    ],
)
def test_king_can_move_via_castle(
    square_to_move_to: str,
    other_pieces: tuple[Piece, str],
    should_be_able_to_move: bool,
) -> None:
    king_location = to_coordinates("E1")

    board = Board({
        king_location: Piece(PieceType.King, Color.White),
        to_coordinates("A1"): Piece(PieceType.Rook, Color.White),
        to_coordinates("H1"): Piece(PieceType.Rook, Color.White),
        ** {
            to_coordinates(square): piece
            for piece, square in other_pieces
        }
    })

    can_move = to_coordinates(square_to_move_to) in get_possible_destinations(
        king_location, board
    )

    assert can_move == should_be_able_to_move


def test_king_cannot_move_via_castle_if_rook_has_moved() -> None:
    king_location = to_coordinates("E1")

    board = Board({
        king_location: Piece(PieceType.King, Color.White),
        to_coordinates("A1"): Piece(PieceType.Rook, Color.White)
    })

    rook_to_a2 = create_move("A1", "A2")
    board.move(rook_to_a2)

    rook_to_a1 = create_move("A2", "A1")
    board.move(rook_to_a1)

    assert to_coordinates("A3") not in get_possible_destinations(
        king_location, board)


def test_king_cannot_move_via_castle_if_king_has_moved() -> None:
    king_location = to_coordinates("E1")

    board = Board({
        king_location: Piece(PieceType.King, Color.White),
        to_coordinates("A1"): Piece(PieceType.Rook, Color.White),
        to_coordinates("H1"): Piece(PieceType.Rook, Color.White)
    })

    king_to_e2 = create_move("E1", "E2")
    board.move(king_to_e2)

    king_to_e1 = create_move("E2", "E1")
    board.move(king_to_e1)

    assert all(
        to_coordinates(square) not in get_possible_destinations(
            king_location, board)
        for square in ["C1", "G1"]
    )
