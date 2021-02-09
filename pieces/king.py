
from __future__ import annotations
from piece import Piece


class King(Piece):
    def __init__(self: King, *args, **kwargs) -> None:
        self.__symbol = '\u2654' if self.__color == 'white' else '\u265A'