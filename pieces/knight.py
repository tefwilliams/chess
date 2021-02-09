
from __future__ import annotations
from piece import Piece


class Knight(Piece):
    def __init__(self: Knight, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__symbol = '\u2658' if self.color == 'white' else '\u265E'

    @property
    def symbol(self: Knight) -> str:
        return self.__symbol
