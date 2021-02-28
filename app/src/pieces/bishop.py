
from __future__ import annotations
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates
from .piece import Piece, PieceTypes


class Bishop(Piece):
    def __init__(self: Bishop, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2657' if self.color == Color.white else '\u265D'

    @property
    def symbol(self: Bishop) -> str:
        return self.__symbol

    def can_move(self: Bishop, coordinates: Coordinates, *args) -> bool:
        return Movement.is_diagonal(self.coordinates, coordinates)

    @property
    def type(self: Bishop) -> PieceTypes:
        return PieceTypes.bishop
        