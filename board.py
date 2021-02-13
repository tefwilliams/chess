
from __future__ import annotations
from pieces.king import King
from pieces.queen import Queen
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.piece import Piece
from coordinates import Coordinates


class Board:
    __shape = Coordinates((8, 8))

    def __init__(self: Board) -> None:
        self.__initialize_pieces()

    def __initialize_pieces(self: Board) -> None:
        pieces: list[Piece] = []

        for i in range(self.__shape.y):
            for j in range(self.__shape.x):
                coordinates = Coordinates((i, j))

                starting_piece = get_starting_piece(coordinates)
                
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

    @property
    def shape(self: Board) -> Coordinates:
        return self.__shape

def get_starting_piece(coordinates: Coordinates) -> Piece | None:
    if coordinates.y in [1, 6]:
        return Pawn(coordinates)

    if coordinates.y in [0, 7]:
        if coordinates.x in [0, 7]:
            return Rook(coordinates)

        if coordinates.x in [1, 6]:
            return Knight(coordinates)

        if coordinates.x in [2, 5]:
            return Bishop(coordinates)

        if coordinates.x == 3:
            return Queen(coordinates)

        if coordinates.x == 4:
            return King(coordinates)
