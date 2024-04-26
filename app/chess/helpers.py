from typing import Iterator, TypeVar
from .data import board_size
from .color import Color
from .vector import Vector


unit_step_up = Vector(-1, 0)
unit_step_right = Vector(0, 1)
unit_step_down = Vector(1, 0)
unit_step_left = Vector(0, -1)

horizontal_unit_steps = [unit_step_right, unit_step_left]

vertical_unit_steps = [unit_step_up, unit_step_down]

orthogonal_unit_steps = horizontal_unit_steps + vertical_unit_steps

diagonal_unit_steps = [
    vertical_step + horizontal_step
    for vertical_step in vertical_unit_steps
    for horizontal_step in horizontal_unit_steps
]

all_unit_steps = orthogonal_unit_steps + diagonal_unit_steps


def get_unit_step_forward(color: Color):
    return unit_step_down if color == Color.White else unit_step_up


def get_unit_step_backward(color: Color):
    return get_unit_step_forward(color.get_opposing_color())


def within_board(coordinates: Vector):
    return 0 <= coordinates.row < board_size and 0 <= coordinates.col < board_size


T = TypeVar("T")


def only(iterator: Iterator[T], error_message: str = "") -> T | None:
    """
    Return the only item from the iterator.
    Returns None the iterator is exhausted.
    Raise RuntimeError with optional error message if more than item in iterator.
    """
    results = [iterator]

    if len(results) > 1:
        raise RuntimeError(error_message)

    return next(iterator, None)


def last(list: list[T]) -> T | None:
    """
    Return the last item in the list.
    Returns None if the list is empty.
    """
    return next(reversed(list), None)
