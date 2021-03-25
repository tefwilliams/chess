
from chess import Board, Coordinates, Color, PieceTypes
from generate_piece import generate_piece


def test_pawn_can_move_one_or_two_forward_if_it_has_not_moved() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    board = Board([pawn])

    assert pawn.get_possible_moves(board).sort() == [Coordinates.convert_from_grid_value('C2'), Coordinates.convert_from_grid_value('B2')].sort()

def test_pawn_can_move_two_forward_if_it_has_not_moved() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    board = Board([pawn])

    assert Coordinates.convert_from_grid_value('C2') in pawn.get_possible_moves(board)

def test_pawn_cannot_move_two_forward_if_it_has_moved() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    board = Board([pawn])

    board.evaluate_move(pawn, Coordinates.convert_from_grid_value('B2'))

    assert Coordinates.convert_from_grid_value('D2') not in pawn.get_possible_moves(board)

def test_pawn_can_move_forward_diagonally_if_enemy_piece_there() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    pieces = [
        pawn,
        generate_piece(PieceTypes.rook, 'B1', Color.black)
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value('B1') in pawn.get_possible_moves(board)

def test_pawn_can_move_via_en_passant_if_enemy_pawn_has_just_moved_two_squares() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'E2', Color.white)
    enemy_pawn = generate_piece(PieceTypes.pawn, 'G1', Color.black)

    pieces = [
        pawn,
        enemy_pawn
    ]

    board = Board(pieces)
    
    board.evaluate_move(enemy_pawn, Coordinates.convert_from_grid_value('E1'))

    assert Coordinates.convert_from_grid_value('F1') in pawn.get_possible_moves(board)

def test_pawn_cannot_move_via_en_passant_if_another_piece_has_moved() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'E2', Color.white)
    enemy_pawn = generate_piece(PieceTypes.pawn, 'G1', Color.black)
    other_enempy_piece = generate_piece(PieceTypes.bishop, 'H5', Color.black)

    pieces = [
        pawn,
        enemy_pawn,
        other_enempy_piece
    ]

    board = Board(pieces)

    board.evaluate_move(enemy_pawn, Coordinates.convert_from_grid_value('E1'))
    board.evaluate_move(other_enempy_piece, Coordinates.convert_from_grid_value('G4'))

    assert Coordinates.convert_from_grid_value('F1') not in pawn.get_possible_moves(board)

def test_pawn_cannot_move_forward_diagonally_if_fiendly_piece_there() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    pieces = [
        pawn,
        generate_piece(PieceTypes.rook, 'B1', Color.white)
    ]

    board = Board(pieces)

    assert Coordinates.convert_from_grid_value('B1') not in pawn.get_possible_moves(board)

def test_pawn_cannot_move_two_forward_diagonally() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'A2', Color.white)

    pieces = [
        pawn,
        generate_piece(PieceTypes.rook, 'C3', Color.black)
    ]

    board = Board(pieces)

    assert not Coordinates.convert_from_grid_value('C3') in pawn.get_possible_moves(board)

def test_pawn_cannot_move_backward() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'B1', Color.white)

    board = Board([pawn])

    assert not Coordinates.convert_from_grid_value('A1') in pawn.get_possible_moves(board)

def test_pawn_cannot_move_out_of_board() -> None:
    pawn = generate_piece(PieceTypes.pawn, 'H2', Color.white)

    board = Board([pawn])

    assert len(pawn.get_possible_moves(board)) == 0