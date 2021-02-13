
from __future__ import annotations
from pieces.pieces import Pieces
from pieces.piece import Piece
from coordinates import Coordinates


class Board:
    shape = Coordinates((8, 8))

    def __init__(self: Board) -> None:
        self.initialize_pieces()

    def initialize_pieces(self: Board) -> None:
        board_dimensions = Board.shape
        pieces: list[Piece] = []

        for i in range(board_dimensions.y):
            for j in range(board_dimensions.x):
                coordinates = Coordinates((i, j))
                starting_piece = Pieces.get_starting_piece(coordinates)
                
                if starting_piece:
                    pieces.append(starting_piece)

        self.__pieces = pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = [piece for piece in self.__pieces if piece.coordinates == coordinates]

        if len(pieces_with_coordinates) == 0:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" % Coordinates.convert_to_grid_value(coordinates))

        return pieces_with_coordinates.pop()

    def move(self: Board, piece: Piece, coordinates: Coordinates) -> None:
        if piece.coordinates == coordinates:
            raise ValueError("Can't move piece to same location")

        if self.__in_check():
            return

        if not self.get_piece(coordinates):
            piece.move(coordinates)

    def __in_check(self: Board) -> bool:
        return False
