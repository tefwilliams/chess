
from __future__ import annotations
from coordinates import Coordinates
from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self: Pawn, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2659' if self.color == 'white' else '\u265F'

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol