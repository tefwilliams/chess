
from __future__ import annotations
from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self: Pawn, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__symbol = '\u2659' if self.color == 'white' else '\u265F'

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol