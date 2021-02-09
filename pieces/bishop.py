
from __future__ import annotations
from piece import Piece


class Knight(Piece):
    def __init__(self: Knight, *args, **kwargs) -> None:
        self.__symbol = '\u2658' if self.__color == 'white' else '\u265E'