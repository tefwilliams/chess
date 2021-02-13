
from __future__ import annotations
from coordinates import Coordinates
from player import Player


class Piece:
    def __init__(self: Piece, coordinates: Coordinates) -> None:
        self.__color: Player = 'white' if coordinates.y in [0, 1] else 'black'
        self.coordinates = coordinates

    def move(self: Piece, coordinates: Coordinates) -> None:
        self.coordinates = coordinates

    @property
    def color(self: Piece) -> Player:
        return self.__color

    @property
    def symbol(self: Piece) -> str:
        ...
