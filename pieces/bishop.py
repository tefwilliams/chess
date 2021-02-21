
from __future__ import annotations
from movement import Movement
from coordinates import Coordinates
from pieces.piece import Piece, PieceTypes


class Bishop(Piece):
    def __init__(self: Bishop, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2657' if self.color == 'white' else '\u265D'

    @property
    def symbol(self: Bishop) -> str:
        return self.__symbol

    def can_move(self: Bishop, coordinates: Coordinates, *args) -> bool:
        return Movement.is_diagonal(self.coordinates, coordinates)

    @property
    def type(self: Bishop) -> PieceTypes:
        return PieceTypes.bishop
        