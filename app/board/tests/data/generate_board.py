from board import Board
from pieces.piece import Piece

def generate_board(pieces: list[Piece]) -> Board:
    board = Board()
    board._Board__pieces = pieces
    return board