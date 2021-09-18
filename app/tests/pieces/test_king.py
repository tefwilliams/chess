
import pytest
from chess import Board, Color, PieceTypes, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


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

    can_move = get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(king)
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

    assert not get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(king)


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

    assert get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(king)


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

    can_move = get_coordinates_from_grid_value(
        square_to_move_to) in board.get_legal_moves(king)

    assert can_move == should_be_able_to_move


def test_king_cannot_move_via_castle_if_rook_has_moved() -> None:
    king = generate_piece(PieceTypes.king, 'A5', Color.white)

    rook = generate_piece(PieceTypes.rook, 'A1', Color.white)

    pieces = [
        king,
        rook
    ]

    board = Board(pieces)

    board.evaluate_move(rook, get_coordinates_from_grid_value('B1'))
    board.evaluate_move(rook, get_coordinates_from_grid_value('A1'))

    assert get_coordinates_from_grid_value(
        'A3') not in board.get_legal_moves(king)


def test_king_cannot_move_via_castle_if_king_has_moved() -> None:
    king = generate_piece(PieceTypes.king, 'A5', Color.white)

    rooks = [
        generate_piece(PieceTypes.rook, 'A1', Color.white),
        generate_piece(PieceTypes.rook, 'A8', Color.white)
    ]

    pieces = [
        king,
        *rooks
    ]

    board = Board(pieces)

    board.evaluate_move(king, get_coordinates_from_grid_value('B5'))
    board.evaluate_move(king, get_coordinates_from_grid_value('A5'))

    assert all(get_coordinates_from_grid_value(square) not
               in board.get_legal_moves(king) for square in ['A3', 'A7'])
