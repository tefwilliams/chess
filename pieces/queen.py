
from __future__ import annotations
from piece import Piece


class Queen(Piece):
    def __init__(self: Queen, *args, **kwargs) -> None:
        self.__symbol = '\u2655' if self.__color == 'white' else '\u265B'