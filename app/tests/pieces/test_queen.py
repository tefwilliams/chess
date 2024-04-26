import pytest
from chess import Board, Color, PieceType, Piece
from ..repository import generate_piece, get_coordinates_from_grid_value


@pytest.mark.parametrize(
    "square_to_move_to, should_be_able_to_move",
    [
        ("A2", False),
        ("E2", False),
        ("B4", True),
        ("F6", True),
        ("C1", True),
        ("E5", True),
        ("G3", True),
    ],
)
def test_queen_can_only_move_diagonally_or_orthogonally(
    square_to_move_to: str, should_be_able_to_move: bool
) -> None:
    queen = generate_piece(PieceType.Queen, "F4", Color.White)

    board = Board([queen])

    can_move = get_coordinates_from_grid_value(
        square_to_move_to
    ) in board.get_possible_moves(queen)
    assert can_move == should_be_able_to_move


@pytest.mark.parametrize(
    "square_to_move_to, obstructing_piece",
    [
        ("B4", generate_piece(PieceType.Pawn, "B4", Color.White)),
        ("F6", generate_piece(PieceType.Rook, "F5", Color.Black)),
        ("C1", generate_piece(PieceType.Bishop, "C1", Color.White)),
        ("C1", generate_piece(PieceType.Queen, "E3", Color.Black)),
        ("E5", generate_piece(PieceType.Pawn, "E5", Color.White)),
        ("D6", generate_piece(PieceType.King, "E5", Color.White)),
        ("G3", generate_piece(PieceType.Rook, "G3", Color.White)),
        ("C7", generate_piece(PieceType.Knight, "C7", Color.White)),
    ],
)
def test_queen_cannot_move_if_obstructed(
    square_to_move_to: str, obstructing_piece: Piece
) -> None:
    queen = generate_piece(PieceType.Queen, "F4", Color.White)

    pieces = [queen, obstructing_piece]

    board = Board(pieces)

    assert not get_coordinates_from_grid_value(
        square_to_move_to
    ) in board.get_possible_moves(queen)


@pytest.mark.parametrize(
    "square_to_move_to, opposing_piece",
    [
        ("B4", generate_piece(PieceType.Pawn, "B4", Color.Black)),
        ("F6", generate_piece(PieceType.Rook, "F6", Color.Black)),
        ("C1", generate_piece(PieceType.Bishop, "C1", Color.Black)),
        ("E3", generate_piece(PieceType.Queen, "E3", Color.Black)),
        ("E5", generate_piece(PieceType.Pawn, "E5", Color.Black)),
        ("G3", generate_piece(PieceType.Rook, "G3", Color.Black)),
        ("C7", generate_piece(PieceType.Knight, "C7", Color.Black)),
    ],
)
def test_queen_can_take_opposing_piece(
    square_to_move_to: str, opposing_piece: Piece
) -> None:
    queen = generate_piece(PieceType.Queen, "F4", Color.White)

    pieces = [queen, opposing_piece]

    board = Board(pieces)

    assert get_coordinates_from_grid_value(
        square_to_move_to
    ) in board.get_possible_moves(queen)
