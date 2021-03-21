
import pytest
from app.src import Board, Coordinates, Color, PieceTypes
from app.tests.data.generate_piece import generate_piece


def supply_king_can_move() -> list[tuple[str, bool]]:
    return [
        ('A2', False),
        ('B1', False),
        ('B4', False),
        ('F6', False),
        ('F3', True),
        ('E5', True),
        ('G4', True)
    ]

@pytest.mark.parametrize("square_to_move_to, should_be_able_to_move", supply_king_can_move())
def test_king_can_only_move_to_adjacent_squares(square_to_move_to: str, should_be_able_to_move: bool) -> None:
    king = generate_piece(PieceTypes.king, 'F4', Color.white)

    board = Board([king])

    can_move = Coordinates.convert_from_grid_value(square_to_move_to) in king.get_possible_moves(board)

    assert can_move == should_be_able_to_move

def test_king_cannot_move_if_obstructed() -> None:
    king = generate_piece(PieceTypes.king, 'A1', Color.white)

    pieces = [
        king,
        generate_piece(PieceTypes.bishop, 'B2', Color.white)
    ]

    board = Board(pieces)

    assert not Coordinates.convert_from_grid_value('E5') in king.get_possible_moves(board)

def test_king_can_take_opposing_piece() -> None:
    king = generate_piece(PieceTypes.king, 'A1', Color.white)

    pieces = [
        king,
        generate_piece(PieceTypes.bishop, 'B2', Color.black)
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value('B2') in king.get_possible_moves(board)
