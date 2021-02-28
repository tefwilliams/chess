
from __future__ import annotations
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates
from .piece import Piece, PieceTypes


class Knight(Piece):
    def __init__(self: Knight, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2658' if self.color == Color.white else '\u265E'

    @property
    def symbol(self: Knight) -> str:
        return self.__symbol

    def can_move(self: Knight, coordinates: Coordinates, *args) -> bool:
        return Movement.is_knight(self.coordinates, coordinates)

    @property
    def type(self: Knight) -> PieceTypes:
        return PieceTypes.knight
