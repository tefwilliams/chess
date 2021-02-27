
from __future__ import annotations
from app.player import Color
from app.movement import Movement
from app.coordinates import Coordinates
from .piece import Piece, PieceTypes


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
