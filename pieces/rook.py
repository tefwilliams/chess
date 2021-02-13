
from __future__ import annotations
from coordinates import Coordinates
from pieces.piece import Piece


class Rook(Piece):
    def __init__(self: Rook, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2656' if self.color == 'white' else '\u265C'

    @property
    def symbol(self: Rook) -> str:
        return self.__symbol