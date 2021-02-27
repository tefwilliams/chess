
from __future__ import annotations
from .piece import Piece
from .king import King
from .queen import Queen
from .bishop import Bishop
from .knight import Knight
from .rook import Rook
from .pawn import Pawn
from ..coordinates import Coordinates


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
                