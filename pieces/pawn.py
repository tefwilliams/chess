
from __future__ import annotations
from movement import Movement
from coordinates import Coordinates
from pieces.piece import Piece, PieceTypes


class Pawn(Piece):
    def __init__(self: Pawn, coordinates: Coordinates) -> None:
        super().__init__(coordinates)
        self.__symbol = '\u2659' if self.player == 'white' else '\u265F'
        self.__starting_coordinates = coordinates

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol

    @property
    def __has_moved(self: Pawn) -> bool:
        return self.coordinates != self.__starting_coordinates

    def can_move(self: Pawn, coordinates: Coordinates, piece_at_destination: Piece | None) -> bool:
        number_of_steps = len(Movement.get_steps(self.coordinates, coordinates))

        if self.__movement_is_backward(coordinates):
            return False

        if number_of_steps == 1:
            if piece_at_destination and Movement.is_diagonal(self.coordinates, coordinates):
                return True

            if not piece_at_destination and Movement.is_vertical(self.coordinates, coordinates):
                return True

        if not self.__has_moved and number_of_steps == 2:
            if not piece_at_destination and Movement.is_vertical(self.coordinates, coordinates):
                return True

        return False

    def move(self: Pawn, coordinates: Coordinates) -> None:
        self.coordinates = coordinates

    def __movement_is_backward(self: Pawn, coordinates: Coordinates) -> bool:
        if not Movement.is_vertical(self.coordinates, coordinates):
            return False

        if self.player == 'white' and self.coordinates.y > coordinates.y:
            return True

        if self.player == 'black' and self.coordinates.y < coordinates.y:
            return True

        return False

    @property
    def type(self: Pawn) -> PieceTypes:
        return PieceTypes.pawn
