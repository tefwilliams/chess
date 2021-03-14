
from ...src.coordinates import Coordinates, Direction


# TODO - look at zero checking for movement
class Movement:
    @staticmethod
    def get_diagonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        diagonal_squares: list[list[Coordinates]] = []

        directions = [Direction((y, x)) for y in [-1, 1] for x in [-1, 1]]

        for direction in directions:
            squares_in_direction: list[Coordinates] = []
            destination_coordinates = direction.step(origin_coordinates)

            while destination_coordinates.within_board:
                squares_in_direction.append(destination_coordinates)
                destination_coordinates = direction.step(destination_coordinates)

            diagonal_squares.append(squares_in_direction)

        return diagonal_squares

    @staticmethod
    def get_orthogonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        orthogonal_squares: list[list[Coordinates]] = []

        directions = [Direction((y, x)) for y in [-1, 0, 1] for x in [-1, 0, 1] if abs(y + x) == 1]

        for direction in directions:
            squares_in_direction: list[Coordinates] = []
            destination_coordinates = direction.step(origin_coordinates)

            while destination_coordinates.within_board:
                squares_in_direction.append(destination_coordinates)
                destination_coordinates = direction.step(destination_coordinates)

            orthogonal_squares.append(squares_in_direction)

        return orthogonal_squares

    @staticmethod
    def get_adjacent_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        adjacent_squares: list[list[Coordinates]] = []

        directions = [Direction((y, x)) for y in [-1, 0, 1] for x in [-1, 0, 1] if not y == x == 0]

        for direction in directions:
            squares_in_direction = [direction.step(origin_coordinates)]
            adjacent_squares.append([square for square in squares_in_direction if square.within_board])

        return adjacent_squares

    @staticmethod
    def get_knight_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        knight_squares: list[list[Coordinates]] = []

        directions = [Direction((y, x)) for y in [-2, -1, 1, 2] for x in [-2, -1, 1, 2] if not y == x and not y == -x]

        for direction in directions:
            squares_in_direction = [direction.step(origin_coordinates)]
            knight_squares.append([square for square in squares_in_direction if square.within_board])

        return knight_squares

    @staticmethod
    def is_horizontal(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        return Movement.__vertical_movement(starting_coordinates, finishing_coordinates) == 0

    @staticmethod
    def is_vertical(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        return Movement.__horizontal_movement(starting_coordinates, finishing_coordinates) == 0

    @staticmethod
    def is_diagonal(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        horizontal_movement = Movement.__horizontal_movement(starting_coordinates, finishing_coordinates)
        vertical_movement = Movement.__vertical_movement(starting_coordinates, finishing_coordinates)

        return horizontal_movement == vertical_movement

    @staticmethod
    def is_knight(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        horizontal_movement = Movement.__horizontal_movement(starting_coordinates, finishing_coordinates)
        vertical_movement = Movement.__vertical_movement(starting_coordinates, finishing_coordinates)

        return (horizontal_movement == 2 and vertical_movement == 1
            or horizontal_movement == 1 and vertical_movement == 2)

    @staticmethod
    def is_adjacent(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        return ((Movement.is_horizontal(starting_coordinates, finishing_coordinates)
            or Movement.is_vertical(starting_coordinates, finishing_coordinates)
            or Movement.is_diagonal(starting_coordinates, finishing_coordinates))
            and len(Movement.get_steps(starting_coordinates, finishing_coordinates)) == 1)


    @staticmethod
    def get_steps(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> list[Coordinates]:
        if Movement.is_horizontal(starting_coordinates, finishing_coordinates):
            return Movement.__get_horizontal_steps(starting_coordinates, finishing_coordinates)

        if Movement.is_vertical(starting_coordinates, finishing_coordinates):
            return Movement.__get_vertical_steps(starting_coordinates, finishing_coordinates)

        if Movement.is_diagonal(starting_coordinates, finishing_coordinates):
            return Movement.__get_diagonal_steps(starting_coordinates, finishing_coordinates)

        if Movement.is_knight(starting_coordinates, finishing_coordinates):
            return [Coordinates(starting_coordinates)]
        
        raise ValueError("Not a valid movement")

    @staticmethod
    def __get_horizontal_steps(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> list[Coordinates]:
        step = 1 if starting_coordinates.x < finishing_coordinates.x else -1

        horizontal_steps = list(range(starting_coordinates.x, finishing_coordinates.x, step))
        vertical_steps = [starting_coordinates.y] * len(horizontal_steps)

        steps = list(zip(vertical_steps, horizontal_steps))

        return [Coordinates(step) for step in steps]

    @staticmethod
    def __get_vertical_steps(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> list[Coordinates]:
        step = 1 if starting_coordinates.y < finishing_coordinates.y else -1

        vertical_steps = list(range(starting_coordinates.y, finishing_coordinates.y, step))
        horizontal_steps = [starting_coordinates.x] * len(vertical_steps)

        steps = list(zip(vertical_steps, horizontal_steps))

        return [Coordinates(step) for step in steps]

    @staticmethod
    def __get_diagonal_steps(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> list[Coordinates]:
        horizontal_step = 1 if starting_coordinates.x < finishing_coordinates.x else -1
        vertical_step = 1 if starting_coordinates.y < finishing_coordinates.y else -1

        horizontal_steps = list(range(starting_coordinates.x, finishing_coordinates.x, horizontal_step))
        vertical_steps = list(range(starting_coordinates.y, finishing_coordinates.y, vertical_step))

        if len(horizontal_steps) != len(vertical_steps):
            raise ValueError("Expected horizontal and vertical steps to be the same length")

        steps = list(zip(vertical_steps, horizontal_steps))

        return [Coordinates(step) for step in steps]

    @staticmethod
    def __horizontal_movement(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> int:
        return abs(finishing_coordinates.x - starting_coordinates.x)

    @staticmethod
    def __vertical_movement(starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> int:
        return abs(finishing_coordinates.y - starting_coordinates.y)
