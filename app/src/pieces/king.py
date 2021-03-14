
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.coordinates import Coordinates
    from ...src.board import Board


class King(Piece):
    def __init__(self: King, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2654' if self.color == Color.white else '\u265A'

    @property
    def symbol(self: King) -> str:
        return self.__symbol

    def can_move(self: King, coordinates: Coordinates, board: Board) -> bool:
        number_of_steps = len(Movement.get_steps(self.coordinates, coordinates))

        if number_of_steps == 1:
            return True

        if self.__movement_is_castle(coordinates, board):
            return True

        return False

    def __movement_is_castle(self: King, coordinates: Coordinates, board: Board) -> bool:
        steps = Movement.get_steps(self.coordinates, coordinates)
        number_of_steps = len(steps)
        last_step = steps.pop()

        is_last_step_attacked = board.is_square_attacked(last_step, self.color)

        return (number_of_steps == 2
            and not self.has_moved
            and Movement.is_horizontal(self.coordinates, coordinates) 
            and not is_last_step_attacked)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        adjacent_squares = Movement.get_adjacent_squares(self.coordinates)
        return board.get_unobstructed_squares(self, adjacent_squares)

    @property
    def type(self: King) -> PieceTypes:
        return PieceTypes.king
        