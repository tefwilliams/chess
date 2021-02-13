
from __future__ import annotations
from coordinates import Coordinates
from pieces.piece import Piece


class Queen(Piece):
    def __init__(self: Queen, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2655' if self.color == 'white' else '\u265B'

    @property
    def symbol(self: Queen) -> str:
        return self.__symbol
