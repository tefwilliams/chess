
from __future__ import annotations
from .piece import Piece, PieceTypes
from ..player import Color
from ..movement import Movement
from ..coordinates import Coordinates


class Rook(Piece):
    def __init__(self: Rook, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2656' if self.color == Color.white else '\u265C'

    @property
    def symbol(self: Rook) -> str:
        return self.__symbol

    def can_move(self: Rook, coordinates: Coordinates, *args) -> bool:
        return (Movement.is_horizontal(self.coordinates, coordinates) 
            or Movement.is_vertical(self.coordinates, coordinates))

    @property
    def type(self: Rook) -> PieceTypes:
        return PieceTypes.rook
