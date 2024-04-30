from .piece import Piece, PieceType
from ..color import Color
from ..vector import Vector


class MovablePiece(Piece):
    def __init__(self, type: PieceType, color: Color, coordinates: Vector):
        self.__type = type
        self.__color = color

        self.__coordinates = coordinates
        self.__coordinates_history: list[Vector] = []

    @property
    def type(self) -> PieceType:
        return self.__type

    @type.setter
    def type(self, value: PieceType):
        self.__type = value

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def coordinates(self) -> Vector:
        return self.__coordinates

    def move(self, new_coordinates: Vector):
        self.__coordinates_history.append(self.coordinates)
        self.__coordinates = new_coordinates

    # TODO - probably can replace these with methods on the board
    # If we can do that - does it make more sense to track all
    # movement directly on the board?

    @property
    def has_moved(self):
        return len(self.__coordinates_history) > 0

    @property
    def coordinates_history(self):
        return tuple(self.__coordinates_history)
