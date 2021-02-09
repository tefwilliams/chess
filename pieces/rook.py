
from __future__ import annotations
from piece import Piece


class Rook(Piece):
    def __init__(self: Rook, *args, **kwargs) -> None:
        self.__symbol = '\u2656' if self.__color == 'white' else '\u265C'