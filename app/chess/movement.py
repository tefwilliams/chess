
from __future__ import annotations
from .player import Color
from .grid import Coordinates, Step, horizontal_unit_steps, orthogonal_unit_steps, diagonal_unit_steps, all_unit_steps, unit_step_left, unit_step_right
from .data import board_size


class Movement:
    @staticmethod
    def get_diagonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        return [Movement.__get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction) for unit_step_in_direction in diagonal_unit_steps]

    @staticmethod
    def get_orthogonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        return [Movement.__get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction) for unit_step_in_direction in orthogonal_unit_steps]

    @staticmethod
    def get_adjacent_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        return [Movement.__get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction, 1) for unit_step_in_direction in all_unit_steps]

    @staticmethod
    def get_knight_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        knight_steps = [orthogonal_step + diagonal_step 
            for orthogonal_step in orthogonal_unit_steps
            for diagonal_step in diagonal_unit_steps
            if not (orthogonal_step + diagonal_step).has_magnitude_one]

        return [Movement.__get_squares_by_repeating_step(origin_coordinates, step, 1) for step in knight_steps]

    @staticmethod
    def get_castle_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        return [Movement.__get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction) for unit_step_in_direction in horizontal_unit_steps]

    @staticmethod
    def get_pawn_squares(origin_coordinates: Coordinates, color: Color, has_moved: bool) -> list[list[Coordinates]]:
        maximum_number_of_steps = 1 if has_moved else 2

        return [Movement.__get_squares_by_repeating_step(origin_coordinates, color.get_step_forward(), maximum_number_of_steps)]

    @staticmethod
    def get_pawn_attack_squares(origin_coordinates: Coordinates, color: Color) -> list[list[Coordinates]]:
        unit_step_forward = color.get_step_forward()
        pawn_attack_steps = [unit_step_forward + unit_step_left, unit_step_forward + unit_step_right]

        return [Movement.__get_squares_by_repeating_step(origin_coordinates, step, 1) for step in pawn_attack_steps]

    @staticmethod
    def __get_squares_by_repeating_step(origin_coordinates: Coordinates, step: Step, number_of_steps: int = board_size) -> list[Coordinates]:
        squares_by_repeating_step = [origin_coordinates.move_by(step * (i + 1)) for i in range(number_of_steps)]
        return [square for square in squares_by_repeating_step if square.within_board]
