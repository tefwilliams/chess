
from __future__ import annotations


class Coordinates(tuple[int, int]):
    maximum_size = 8 # TODO - Consider name
    y_grid_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    x_grid_values = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self: Coordinates, coordinates: tuple[int, int]) -> None:
        self.x = coordinates[1]
        self.y = coordinates[0]

    @property
    def within_board(self: Coordinates) -> bool:
        return self.y >= 0 and self.x >= 0 and self.y < Coordinates.maximum_size and self.x < Coordinates.maximum_size

    @staticmethod
    def get_coordinates(input_text: str) -> Coordinates:
        while True:
            try:
                coordinates_as_string = input(input_text).upper()
                return Coordinates.convert_from_grid_value(coordinates_as_string)

            except ValueError as e:
                print("\n" + "%s" % e)

    @staticmethod
    def convert_from_grid_value(coordinates: str) -> Coordinates:
        if not Coordinates.__validate_coordinates(coordinates):
            raise ValueError("Invalid coordinates")

        y_value = Coordinates.y_grid_values.index(coordinates[0])
        x_value = Coordinates.x_grid_values.index(coordinates[1])

        return Coordinates((y_value, x_value))

    @staticmethod
    def convert_to_grid_value(coordinates: Coordinates) -> str:
        y_value = Coordinates.y_grid_values[coordinates[0]]
        x_value = Coordinates.x_grid_values[coordinates[1]]

        coordinates_as_grid_value = "%s%s" % (y_value, x_value)

        if not Coordinates.__validate_coordinates(coordinates_as_grid_value):
            raise ValueError("Invalid coordinates")

        return coordinates_as_grid_value

    @staticmethod
    def __validate_coordinates(coordinates: str) -> bool:
        if len(coordinates) != 2:
            return False

        if coordinates[0] not in Coordinates.y_grid_values:
            return False

        if coordinates[1] not in Coordinates.x_grid_values:
            return False

        return True

class Direction(Coordinates):
    @property
    def is_vertical(self: Direction) -> bool:
        return self.x == 0

    @property
    def is_horizontal(self: Direction) -> bool:
        return self.y == 0

    @property
    def is_diagonal(self: Direction) -> bool:
        return abs(self.y) == abs(self.x)

    def step(self: Direction, starting_coordinates: Coordinates) -> Coordinates:
        return Coordinates((self.y + starting_coordinates.y, self.x + starting_coordinates.x))
