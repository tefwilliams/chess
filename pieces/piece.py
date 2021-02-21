
from __future__ import annotations
from enum import Enum
from coordinates import Coordinates
from player import Player


class Piece:
    __player: Player

    def __init__(self: Piece, coordinates: Coordinates) -> None:
        self.__player = Player.white if coordinates.y in [0, 1] else Player.black
        self.coordinates = coordinates

    def move(self: Piece, coordinates: Coordinates) -> None:
        self.coordinates = coordinates

    def can_move(self: Piece, coordinates: Coordinates, piece_at_destination: Piece | None) -> bool:
        ...

    @property
    def player(self: Piece) -> Player:
        return self.__player

    # Is this properly abstracted?
    @property
    def symbol(self: Piece) -> str:
        ...

    @property
    def type(self: Piece) -> PieceTypes:
        ...

class PieceTypes(Enum):
    king = 0
    queen = 1
    bishop = 2
    knight = 3
    rook = 4
    pawn = 5
