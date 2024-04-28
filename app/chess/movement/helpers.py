from ..color import Color
from ..board import board_size
from .unit_steps import (
    horizontal_unit_steps,
    orthogonal_unit_steps,
    diagonal_unit_steps,
    all_unit_steps,
    unit_step_left,
    unit_step_right,
    get_unit_step_forward,
)
from ..vector import Vector


def get_diagonal_squares(origin_coordinates: Vector) -> list[list[Vector]]:
    return [
        get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction)
        for unit_step_in_direction in diagonal_unit_steps
    ]


def get_orthogonal_squares(origin_coordinates: Vector) -> list[list[Vector]]:
    return [
        get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction)
        for unit_step_in_direction in orthogonal_unit_steps
    ]


def get_adjacent_squares(origin_coordinates: Vector) -> list[list[Vector]]:
    return [
        get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction, 1)
        for unit_step_in_direction in all_unit_steps
    ]


def get_knight_squares(origin_coordinates: Vector) -> list[list[Vector]]:
    knight_steps = [
        step
        for step in (
            orthogonal_step + diagonal_step
            for orthogonal_step in orthogonal_unit_steps
            for diagonal_step in diagonal_unit_steps
        )
        if step.row + step.col == 4
    ]

    return [
        get_squares_by_repeating_step(origin_coordinates, step, 1)
        for step in knight_steps
    ]


def get_castle_squares(origin_coordinates: Vector) -> list[list[Vector]]:
    return [
        get_squares_by_repeating_step(origin_coordinates, unit_step_in_direction)
        for unit_step_in_direction in horizontal_unit_steps
    ]


def get_pawn_squares(
    origin_coordinates: Vector, color: Color, has_moved: bool
) -> list[list[Vector]]:
    maximum_number_of_steps = 1 if has_moved else 2

    return [
        get_squares_by_repeating_step(
            origin_coordinates, get_unit_step_forward(color), maximum_number_of_steps
        )
    ]


def get_pawn_attack_squares(
    origin_coordinates: Vector, color: Color
) -> list[list[Vector]]:
    unit_step_forward = get_unit_step_forward(color)
    pawn_attack_steps = [
        unit_step_forward + unit_step_left,
        unit_step_forward + unit_step_right,
    ]

    return [
        get_squares_by_repeating_step(origin_coordinates, step, 1)
        for step in pawn_attack_steps
    ]


def get_squares_by_repeating_step(
    start: Vector, step: Vector, number_of_steps: int = board_size
) -> list[Vector]:
    return [
        square
        for square in [start + step * (i + 1) for i in range(number_of_steps)]
        if square
    ]
