
from __future__ import annotations
from ..data import board_size, board_edge_thickness, board_border_thickness, square_size
from math import floor


class Coordinates(tuple[int, int]):
    y_grid_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    x_grid_values = ['8', '7', '6', '5', '4', '3', '2', '1']

    def __new__(cls: type[Coordinates], y_coordinate: int, x_coordinate: int) -> Coordinates:
        return super().__new__(cls, (y_coordinate, x_coordinate))

    def __init__(self: Coordinates, y_coordinate: int, x_coordinate: int) -> None:
        self.x = x_coordinate
        self.y = y_coordinate

    @property
    def within_board(self: Coordinates) -> bool:
        return self.y >= 0 and self.x >= 0 and self.y < board_size and self.x < board_size

    def move_by(self: Coordinates, step: tuple[int, int]) -> Coordinates:
        step = Coordinates(*step)
        return Coordinates(self.y + step.y, self.x + step.x)

    @staticmethod
    def get_coordinates(input_text: str) -> Coordinates:
        while True:
            try:
                coordinates_as_string = input(input_text).upper()
                return Coordinates.convert_from_grid_value(coordinates_as_string)

            except ValueError as e:
                print("\n" + "%s" % e)

    @staticmethod
    def get_coordinates_from_mouse_position(x_position: int, y_position: int) -> Coordinates:
        x_coord = Coordinates.__get_coordinate_from_position(x_position)
        y_coord = Coordinates.__get_coordinate_from_position(y_position)
        return Coordinates(y_coord, x_coord)

    @staticmethod
    def __get_coordinate_from_position(position: int) -> int:
        return floor((position - board_edge_thickness -
                      board_border_thickness * 2) / square_size)

    @staticmethod
    def convert_from_grid_value(coordinates: str) -> Coordinates:
        if not Coordinates.__validate_coordinates(coordinates):
            raise ValueError("Invalid coordinates")

        y_value = Coordinates.y_grid_values.index(coordinates[0])
        x_value = Coordinates.x_grid_values.index(coordinates[1])

        return Coordinates(y_value, x_value)

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
