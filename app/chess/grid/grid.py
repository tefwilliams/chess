
from __future__ import annotations
from typing import TypeVar

class Grid(tuple[int, int]):
    def __init__(self: Grid, values: tuple[int, int] = (0, 0)) -> None:
        y_value, x_value = values

        self.x = x_value
        self.y = y_value

    def __add__(self: T, other: T) -> T:
        return self.__class__((self.y + other.y, self.x + other.x))

    def __mul__(self: T, mutiple: int) -> T:
        return self.__class__((self.y * mutiple, self.x * mutiple))

T = TypeVar('T', bound=Grid)
