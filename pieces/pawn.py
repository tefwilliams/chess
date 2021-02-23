
from __future__ import annotations
from movement import Movement
from pieces.piece import Piece, PieceTypes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coordinates import Coordinates
    from board import Board


class Pawn(Piece):
    def __init__(self: Pawn, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2659' if self.color == 'white' else '\u265F'
        self.__starting_coordinates = coordinates

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol

    # @property
    # def __has_moved(self: Pawn) -> bool:
    #     return self.coordinates != self.__starting_coordinates

    def can_move(self: Pawn, coordinates: Coordinates, board: Board) -> bool:
        piece_at_destination = board.get_piece(coordinates)
        number_of_steps = len(Movement.get_steps(self.coordinates, coordinates))

        if self.__movement_is_backward(coordinates):
            return False

        if number_of_steps == 1:
            if piece_at_destination and Movement.is_diagonal(self.coordinates, coordinates):
                return True

            if not piece_at_destination and Movement.is_vertical(self.coordinates, coordinates):
                return True

        if not self.has_moved and number_of_steps == 2:
            if not piece_at_destination and Movement.is_vertical(self.coordinates, coordinates):
                return True

        return False

    def __movement_is_backward(self: Pawn, coordinates: Coordinates) -> bool:
        if not Movement.is_vertical(self.coordinates, coordinates):
            return False

        if self.color == 'white' and self.coordinates.y > coordinates.y:
            return True

        if self.color == 'black' and self.coordinates.y < coordinates.y:
            return True

        return False

    @property
    def type(self: Pawn) -> PieceTypes:
        return PieceTypes.pawn
