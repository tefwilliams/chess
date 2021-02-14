
from __future__ import annotations
from coordinates import Coordinates
from player import Player
import board


class Piece:
    def __init__(self: Piece, coordinates: Coordinates) -> None:
        self.__color: Player = 'white' if coordinates.y in [0, 1] else 'black'
        self.coordinates = coordinates

    # Will need to abstract this
    def move(self: Piece, coordinates: Coordinates, board: board.Board) -> None:
        if not self.can_move(coordinates, board):
            raise ValueError("Cannot move to that square")

        self.coordinates = coordinates

    def can_move(self: Piece, coordinates: Coordinates, board: board.Board) -> bool:
        ...

    @property
    def color(self: Piece) -> Player:
        return self.__color

    # Is this properly abstracted?
    @property
    def symbol(self: Piece) -> str:
        ...
