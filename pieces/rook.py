
from __future__ import annotations
from piece import Piece


class Rook(Piece):
    def __init__(self: Rook, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__symbol = '\u2656' if self.color == 'white' else '\u265C'

    @property
    def symbol(self: Rook) -> str:
        return self.__symbol