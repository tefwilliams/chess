
from __future__ import annotations
from piece import Piece


class Queen(Piece):
    def __init__(self: Queen, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__symbol = '\u2655' if self.color == 'white' else '\u265B'

    @property
    def symbol(self: Queen) -> str:
        return self.__symbol
