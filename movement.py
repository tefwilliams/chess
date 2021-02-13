

from coordinates import Coordinates


class Movement:
    @staticmethod
    def is_horizontal(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        return starting_coordinates.y == finishing_coordinates.y

    @staticmethod
    def is_vertical(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        return starting_coordinates.x == finishing_coordinates.x

    @staticmethod
    def is_diagonal(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        horizontal_movement = abs(finishing_coordinates.x - starting_coordinates.x)
        vertical_movement = abs(finishing_coordinates.y - starting_coordinates.y)

        return horizontal_movement == vertical_movement

    @staticmethod
    def is_knight(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        horizontal_movement = abs(finishing_coordinates.x - starting_coordinates.x)
        vertical_movement = abs(finishing_coordinates.y - starting_coordinates.y)

        return (horizontal_movement == 2 and vertical_movement == 1
            or horizontal_movement == 1 and vertical_movement == 2)