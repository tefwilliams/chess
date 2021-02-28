
from __future__ import annotations
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates
from .piece import Piece, PieceTypes


class Queen(Piece):
    def __init__(self: Queen, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
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
