from __future__ import annotations


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
