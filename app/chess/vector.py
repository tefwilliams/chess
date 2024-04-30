from __future__ import annotations
from copy import deepcopy


class Vector(tuple[int, int]):
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __new__(cls, row: int, col: int):
        return super().__new__(cls, (row, col))

    def __add__(self, other: Vector | int) -> Vector:
        if type(other) is int:
            return Vector(self.row + other, self.col + other)

        if type(other) is Vector:
            return Vector(self.row + other.row, self.col + other.col)

        raise ValueError("Addition must be either Vector or int")

    def __mul__(self, mutiple: int) -> Vector:
        return Vector(self.row * mutiple, self.col * mutiple)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls, self.row, self.col)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
