
from __future__ import annotations
from abc import abstractproperty
from player import Player


class Piece:
    def __init__(self: Piece, color: Player = 'white', *args, **kwargs) -> None:
        self.__color = color

    @property
    def color(self: Piece):
        return self.__color

    @abstractproperty
    def symbol(self: Piece) -> str:
        ...