
from __future__ import annotations
from piece import Piece


class Pawn(Piece):
    def __init__(self: Pawn, *args, **kwargs) -> None:
        self.__symbol = '\u2659' if self.__color == 'white' else '\u265F'