
from __future__ import annotations
from typing import TYPE_CHECKING
from app.player import Color
from app.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from app.coordinates import Coordinates
    from app.board import Board


class King(Piece):
    def __init__(self: King, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2654' if self.color == Color.white else '\u265A'

    @property
    def symbol(self: King) -> str:
        return self.__symbol

    def can_move(self: King, coordinates: Coordinates, board: Board) -> bool:
        number_of_steps = len(Movement.get_steps(self.coordinates, coordinates))

        if number_of_steps == 1:
            return True

        if self.__is_castle(coordinates, board):
            return True

        return False

    def __is_castle(self: King, coordinates: Coordinates, board: Board) -> bool:
        steps = Movement.get_steps(self.coordinates, coordinates)
        number_of_steps = len(steps)
        last_step = steps.pop()

        is_last_step_attacked = board.is_square_attacked(last_step, self.color)

        return (number_of_steps == 2
            and not self.has_moved
            and Movement.is_horizontal(self.coordinates, coordinates) 
            and not is_last_step_attacked)

    @property
    def type(self: King) -> PieceTypes:
        return PieceTypes.king
        