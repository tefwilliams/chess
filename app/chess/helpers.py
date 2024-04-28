from typing import Iterator, TypeVar
from .data import board_size
from .vector import Vector


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
