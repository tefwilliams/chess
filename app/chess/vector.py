from __future__ import annotations
from copy import deepcopy


class Vector(tuple[int, int]):
    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row

    def __new__(cls, col: int, row: int):
        return super().__new__(cls, (col, row))

    def __add__(self, other: Vector | int) -> Vector:
        if type(other) is int:
            return Vector(self.col + other, self.row + other)

        if type(other) is Vector:
            return Vector(self.col + other.col, self.row + other.row)

        raise ValueError("Addition must be either Vector or int")

    def __mul__(self, mutiple: int) -> Vector:
        return Vector(self.col * mutiple, self.row * mutiple)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls, self.col, self.row)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
