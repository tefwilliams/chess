
import pytest
from chess import Board, Coordinates, Color, PieceTypes, Piece
from generate_piece import generate_piece


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ('A2', False),
        ('B1', False),
        ('B4', False),
        ('F6', False),
        ('F3', True),
        ('E5', True),
        ('G4', True),
        ('E4', True)
    ]
)
def test_king_can_only_move_to_adjacent_squares(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    king = generate_piece(PieceTypes.king, 'F4', Color.white)

    board = Board([king])

    can_move = Coordinates.convert_from_grid_value(
        square_to_move_to) in king.get_possible_moves(board)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ('F3', generate_piece(PieceTypes.bishop, 'F3', Color.white)),
        ('E5', generate_piece(PieceTypes.rook, 'E5', Color.white)),
        ('G4', generate_piece(PieceTypes.queen, 'G4', Color.white)),
        ('E4', generate_piece(PieceTypes.pawn, 'E4', Color.white))
    ]
)
def test_king_cannot_move_if_obstructed(square_to_move_to: str, obstructing_piece: Piece) -> None:
    king = generate_piece(PieceTypes.king, 'F4', Color.white)

    pieces = [
        king,
        obstructing_piece
    ]

    board = Board(pieces)

    assert not Coordinates.convert_from_grid_value(
        square_to_move_to) in king.get_possible_moves(board)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ('F3', generate_piece(PieceTypes.bishop, 'F3', Color.black)),
        ('E5', generate_piece(PieceTypes.rook, 'E5', Color.black)),
        ('G4', generate_piece(PieceTypes.queen, 'G4', Color.black)),
        ('E4', generate_piece(PieceTypes.pawn, 'E4', Color.black))
    ]
)
def test_king_can_take_opposing_piece(square_to_move_to: str, opposing_piece: Piece) -> None:
    king = generate_piece(PieceTypes.king, 'F4', Color.white)

    pieces = [
        king,
        opposing_piece
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value(
        square_to_move_to) in king.get_possible_moves(board)


@pytest.mark.parametrize(
    "square_to_move_to, other_pieces, should_be_able_to_move",
    [
        ('A3', [], True),
        ('A7', [generate_piece(PieceTypes.rook, 'E5', Color.black)], False),
        ('A3', [generate_piece(PieceTypes.rook, 'E5', Color.black)], False),
        ('A7', [generate_piece(PieceTypes.rook, 'E4', Color.black)], True),
        ('A3', [generate_piece(PieceTypes.rook, 'E4', Color.black)], False),
        ('A2', [generate_piece(PieceTypes.rook, 'E7', Color.black)], False)
    ]
)
def test_king_can_move_via_castle(square_to_move_to: str, other_pieces: list[Piece], should_be_able_to_move: bool) -> None:
    king = generate_piece(PieceTypes.king, 'A5', Color.white)

    rooks = [
        generate_piece(PieceTypes.rook, 'A1', Color.white),
        generate_piece(PieceTypes.rook, 'A8', Color.white)
    ]

    pieces = [
        king,
        *rooks,
        *other_pieces
    ]

    board = Board(pieces)

    can_move = Coordinates.convert_from_grid_value(
        square_to_move_to) in king.get_possible_moves(board)

    assert can_move == should_be_able_to_move
