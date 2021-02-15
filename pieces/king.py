
from __future__ import annotations
from movement import Movement
from coordinates import Coordinates
from pieces.piece import Piece, PieceTypes


class King(Piece):
    def __init__(self: King, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2654' if self.player == 'white' else '\u265A'

    @property
    def symbol(self: King) -> str:
        return self.__symbol

    def can_move(self: King, coordinates: Coordinates, *args) -> bool:
        number_of_steps = len(Movement.get_steps(self.coordinates, coordinates))

        if number_of_steps == 1:
            return True

        return False

    @property
    def type(self: King) -> PieceTypes:
        return PieceTypes.king
        