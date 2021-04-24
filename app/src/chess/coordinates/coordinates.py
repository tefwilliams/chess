
from __future__ import annotations
from ..data import board_size, board_edge_thickness, board_border_thickness, square_size
from math import floor


class Coordinates(tuple[int, int]):
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
    def get_coordinates_from_mouse_position(x_position: int, y_position: int) -> Coordinates:
        x_coord = Coordinates.__get_coordinate_from_position(x_position)
        y_coord = Coordinates.__get_coordinate_from_position(y_position)
        return Coordinates(y_coord, x_coord)

    @staticmethod
    def __get_coordinate_from_position(position: int) -> int:
        return floor((position - board_edge_thickness -
                      board_border_thickness * 2) / square_size)
