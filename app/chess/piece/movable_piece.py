from .piece import Piece
from ..vector import Vector


class MovablePiece:
    def __init__(self, piece: Piece, coordinates: Vector) -> None:
        self.__piece = piece
        self.__coordinates = coordinates

    @property
    def piece(self):
        return self.__piece

    @property
    def coordinates(self):
        return self.__coordinates
