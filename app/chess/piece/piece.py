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
    def __init__(self, type: PieceType, color: Color, coordinates: Vector):
        self.__type = type
        self.__color = color

        self._coordinates = coordinates
        self._coordinates_history: list[Vector] = []

    @property
    def type(self) -> PieceType:
        return self.__type

    @property
    def color(self) -> Color:
        return self.__color
