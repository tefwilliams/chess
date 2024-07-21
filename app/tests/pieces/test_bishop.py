import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import to_coordinates, get_possible_destinations


@pytest.mark.parametrize(
    "color",
    [
        Color.White,
        Color.Black,
    ],
)
def test_bishop_can_only_move_diagonally(color: Color) -> None:
    bishop_location = to_coordinates("F4")

    board = Board({
        bishop_location: Piece(PieceType.Bishop, color),
    })

    assert {
        to_coordinates("B8"),
        to_coordinates("C7"),
        to_coordinates("D6"),
        to_coordinates("E5"),
        to_coordinates("G3"),
        to_coordinates("H2"),
        to_coordinates("C1"),
        to_coordinates("D2"),
        to_coordinates("E3"),
        to_coordinates("G5"),
        to_coordinates("H6"),
    } == get_possible_destinations(bishop_location, board)


@pytest.mark.parametrize(
    "destination, obstructing_piece, obstructing_piece_location",
    [
        ("C1", Piece(PieceType.Bishop, Color.White), "C1"),
        ("C1", Piece(PieceType.Queen, Color.Black), "E3"),
        ("E5", Piece(PieceType.Pawn, Color.White), "E5"),
        ("D6", Piece(PieceType.King, Color.White), "E5"),
        ("G3", Piece(PieceType.Rook, Color.White), "G3"),
        ("C7", Piece(PieceType.Knight, Color.White), "C7"),
    ],
)
def test_bishop_cannot_move_if_obstructed(
    destination: str, obstructing_piece: Piece, obstructing_piece_location: str
) -> None:
    bishop_location = to_coordinates("F4")

    board = Board({
        bishop_location: Piece(PieceType.Bishop, Color.White),
        to_coordinates(obstructing_piece_location): obstructing_piece
    })

    assert not to_coordinates(
        destination) in get_possible_destinations(bishop_location, board)


@pytest.mark.parametrize(
    "destination, opposing_piece, opposing_piece_location",
    [
        ("C1", Piece(PieceType.Bishop, Color.White), "C1"),
        ("C1", Piece(PieceType.Queen, Color.Black), "E3"),
        ("E5", Piece(PieceType.Pawn, Color.White), "E5"),
        ("D6", Piece(PieceType.King, Color.White), "E5"),
        ("G3", Piece(PieceType.Rook, Color.White), "G3"),
        ("C7", Piece(PieceType.Knight, Color.White), "C7"),
    ],
)
def test_bishop_can_take_opposing_piece(
    destination: str, opposing_piece: Piece, opposing_piece_location: str
) -> None:
    bishop_location = to_coordinates("F4")

    board = Board({
        bishop_location: Piece(PieceType.Bishop, Color.White),
        to_coordinates(opposing_piece_location): opposing_piece
    })

    assert not to_coordinates(
        destination) in get_possible_destinations(bishop_location, board)
