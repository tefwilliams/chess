from enum import Enum
from .color import Color


class PieceType(Enum):
    King = 0
    Queen = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Pawn = 5


class Piece:
    def __init__(self, type: PieceType, color: Color):
        self.__type = type
        self.__color = color

    @property
    def type(self) -> PieceType:
        return self.__type

    @property
    def color(self) -> Color:
        return self.__color
