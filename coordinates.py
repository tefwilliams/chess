
from __future__ import annotations


class Coordinates(tuple[int, int]):
    def __init__(self: Coordinates, coordinates: tuple[int, int]) -> None:
        self.x = coordinates[1]
        self.y = coordinates[0]

    @staticmethod
    def convert_to_coordinates(coordinates: str) -> Coordinates:
        if not Coordinates.__validate_coordinates(coordinates):
            raise ValueError("Invalid coordinates")

        y_grid_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        x_grid_values = ['1', '2', '3', '4', '5', '6', '7', '8']

        y_value = y_grid_values.index(coordinates[0])
        x_value = x_grid_values.index(coordinates[1])

        return Coordinates((y_value, x_value))

    @staticmethod
    def __validate_coordinates(coordinates: str) -> bool:
        if len(coordinates) != 2:
            return False

        if coordinates[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            return False

        if coordinates[1] not in ['1', '2', '3', '4', '5', '6', '7', '8']:
            return False

        return True
