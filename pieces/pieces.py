
from __future__ import annotations
from coordinates import Coordinates
from pieces.piece import Piece
from pieces.king import King
from pieces.queen import Queen
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn


class Pieces:
    @staticmethod
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

        raise ValueError("No piece at %s" % coordinates)