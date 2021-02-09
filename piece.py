
from __future__ import annotations
from abc import abstractproperty
from typing import Union
from repository import PieceTypes

Color = 'white' or 'black'


class Piece:
    def __init__(self: Piece, color = 'white', *args, **kwargs) -> None:
        self.__color = color

    @property
    def color(self: Piece):
        return self.__color

    @abstractproperty
    def symbol(self: Piece) -> str:
        ...