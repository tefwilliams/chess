
import pytest
from chess import Board, Coordinates, Color, PieceTypes, Piece
from generate_piece import generate_piece


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move", 
    [
        ('A2', False),
        ('E2', False),
        ('B4', True),
        ('F6', True),
        ('C1', True),
        ('E5', True),
        ('G3', True)
    ]
)
def test_queen_can_only_move_diagonally_or_orthogonally(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    queen = generate_piece(PieceTypes.queen, 'F4', Color.white)

    board = Board([queen])

    can_move = Coordinates.convert_from_grid_value(square_to_move_to) in queen.get_possible_moves(board)
    assert can_move == should_be_able_to_move

@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ('B4', generate_piece(PieceTypes.pawn, 'B4', Color.white)),
        ('F6', generate_piece(PieceTypes.rook, 'F5', Color.black)),
        ('C1', generate_piece(PieceTypes.bishop, 'C1', Color.white)),
        ('C1', generate_piece(PieceTypes.queen, 'E3', Color.black)),
        ('E5', generate_piece(PieceTypes.pawn, 'E5', Color.white)),
        ('D6', generate_piece(PieceTypes.king, 'E5', Color.white)),
        ('G3', generate_piece(PieceTypes.rook, 'G3', Color.white)),
        ('C7', generate_piece(PieceTypes.knight, 'C7', Color.white))
    ]
)
def test_queen_cannot_move_if_obstructed(square_to_move_to: str, obstructing_piece: Piece) -> None:
    queen = generate_piece(PieceTypes.queen, 'F4', Color.white)

    pieces = [
        queen,
        obstructing_piece
    ]

    board = Board(pieces)

    assert not Coordinates.convert_from_grid_value(square_to_move_to) in queen.get_possible_moves(board)

@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ('B4', generate_piece(PieceTypes.pawn, 'B4', Color.black)),
        ('F6', generate_piece(PieceTypes.rook, 'F6', Color.black)),
        ('C1', generate_piece(PieceTypes.bishop, 'C1', Color.black)),
        ('E3', generate_piece(PieceTypes.queen, 'E3', Color.black)),
        ('E5', generate_piece(PieceTypes.pawn, 'E5', Color.black)),
        ('G3', generate_piece(PieceTypes.rook, 'G3', Color.black)),
        ('C7', generate_piece(PieceTypes.knight, 'C7', Color.black))
    ]
)
def test_queen_can_take_opposing_piece(square_to_move_to: str, opposing_piece: Piece) -> None:
    queen = generate_piece(PieceTypes.queen, 'F4', Color.white)

    pieces = [
        queen,
        opposing_piece
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value(square_to_move_to) in queen.get_possible_moves(board)
