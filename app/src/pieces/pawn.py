
from __future__ import annotations
from typing import TYPE_CHECKING
from ...src.player import Color
from ...src.movement import Movement
from ...src.coordinates import Coordinates, Direction
from .piece import Piece, PieceTypes

if TYPE_CHECKING:
    from ...src.board import Board


class Pawn(Piece):
    def __init__(self: Pawn, coordinates: Coordinates, color: Color) -> None:
        super().__init__(coordinates, color)
        self.__symbol = '\u2659' if self.color == Color.white else '\u265F'

    @property
    def symbol(self: Pawn) -> str:
        return self.__symbol

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

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        possible_moves: list[list[Coordinates]] = []
        vertical_direction = 1 if self.color == Color.white else -1

        directions = [Direction((y, x)) for y in [vertical_direction] for x in [-1, 0, 1]]

        for direction in directions:
            moves_in_direction: list[Coordinates] = []
            adjacent_square_in_direction = direction.step(self.coordinates)
            piece_at_destination = board.get_piece(adjacent_square_in_direction)

            if direction.is_vertical and not piece_at_destination:
                moves_in_direction.append(adjacent_square_in_direction)

                if not self.has_moved:
                    square_two_forward = direction.step(adjacent_square_in_direction)

                    if not board.get_piece(square_two_forward):
                        moves_in_direction.append(square_two_forward)

            elif direction.is_diagonal and piece_at_destination:
                moves_in_direction.append(adjacent_square_in_direction)

            possible_moves.append(moves_in_direction)

        return board.get_unobstructed_squares(self, possible_moves)

    @property
    def type(self: Pawn) -> PieceTypes:
        return PieceTypes.pawn
