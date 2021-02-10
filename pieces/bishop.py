
from __future__ import annotations
from pieces.piece import Piece


class Bishop(Piece):
    def __init__(self: Bishop, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__symbol = '\u2657' if self.color == 'white' else '\u265D'

    @property
    def symbol(self: Bishop) -> str:
        return self.__symbol
        