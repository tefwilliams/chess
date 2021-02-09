
from __future__ import annotations
from repository import PieceTypes

Color = 'white' or 'black'


class Piece:
    __symbol: str

    def __init__(self: Piece, type: PieceTypes, color = 'white', *args, **kwargs) -> None:
        self.__type = type
        self.__color = color

    @property
    def type(self: Piece) -> PieceTypes:
        return self.__type

    @property
    def symbol(self: Piece) -> str:
        return self.__symbol