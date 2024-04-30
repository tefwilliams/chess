from enum import Enum
from ..color import Color
from ..vector import Vector


class PieceType(Enum):
    King = 0
    Queen = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Pawn = 5


class Piece:
    @property
    def type(self) -> PieceType:
        raise NotImplementedError()

    @property
    def color(self) -> Color:
        raise NotImplementedError()

    @property
    def coordinates(self) -> Vector:
        raise NotImplementedError()

    @property
    def has_moved(self):
        raise NotImplementedError()

    @property
    def coordinates_history(self):
        raise NotImplementedError()
