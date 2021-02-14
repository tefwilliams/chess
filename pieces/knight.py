
from __future__ import annotations
from movement import Movement
from coordinates import Coordinates
from pieces.piece import Piece


class Knight(Piece):
    def __init__(self: Knight, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2658' if self.color == 'white' else '\u265E'

    @property
    def symbol(self: Knight) -> str:
        return self.__symbol

    def can_move(self: Knight, coordinates: Coordinates) -> bool:
        return Movement.is_knight(self.coordinates, coordinates)
