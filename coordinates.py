
from __future__ import annotations


class Coordinates(tuple[int, int]):
    def __init__(self: Coordinates, coordinates: tuple[int, int]) -> None:
        self.x = coordinates[1]
        self.y = coordinates[0]
