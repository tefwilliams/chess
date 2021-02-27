
from __future__ import annotations
from .piece import Piece, PieceTypes
from ..player import Color
from ..movement import Movement
from ..coordinates import Coordinates


class Queen(Piece):
    def __init__(self: Queen, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2655' if self.color == Color.white else '\u265B'

    @property
    def symbol(self: Queen) -> str:
        return self.__symbol

    def can_move(self: Queen, coordinates: Coordinates, *args) -> bool:
        return (Movement.is_horizontal(self.coordinates, coordinates) 
            or Movement.is_vertical(self.coordinates, coordinates) 
            or Movement.is_diagonal(self.coordinates, coordinates))

    @property
    def type(self: Queen) -> PieceTypes:
        return PieceTypes.queen