
from __future__ import annotations
from ...src.player import Color
from ...src.coordinates import Coordinates
from .piece import Piece
from .king import King
from .queen import Queen
from .bishop import Bishop
from .knight import Knight
from .rook import Rook
from .pawn import Pawn


class Pieces:
    @staticmethod
    def get_starting_piece(coordinates: Coordinates) -> Piece | None:
        color = Color.white if coordinates.y in [0, 1] else Color.black

        if coordinates.y in [1, 6]:
            return Pawn(coordinates, color)

        if coordinates.y in [0, 7]:
            if coordinates.x in [0, 7]:
                return Rook(coordinates, color)

            if coordinates.x in [1, 6]:
                return Knight(coordinates, color)

            if coordinates.x in [2, 5]:
                return Bishop(coordinates, color)

            if coordinates.x == 3:
                return Queen(coordinates, color)

            if coordinates.x == 4:
                return King(coordinates, color)
                