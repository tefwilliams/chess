
from __future__ import annotations
from .piece import Piece, PieceTypes
from ..player import Color
from ..movement import Movement
from ..coordinates import Coordinates


class Knight(Piece):
    def __init__(self: Knight, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2658' if self.color == Color.white else '\u265E'

    @property
    def symbol(self: Knight) -> str:
        return self.__symbol

    def can_move(self: Knight, coordinates: Coordinates, *args) -> bool:
        return Movement.is_knight(self.coordinates, coordinates)

    @property
    def type(self: Knight) -> PieceTypes:
        return PieceTypes.knight
