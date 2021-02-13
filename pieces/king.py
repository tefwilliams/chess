
from __future__ import annotations
from coordinates import Coordinates
from pieces.piece import Piece


class King(Piece):
    def __init__(self: King, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2654' if self.color == 'white' else '\u265A'

    @property
    def symbol(self: King) -> str:
        return self.__symbol
        