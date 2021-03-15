
from ...src.coordinates import Coordinates, Direction


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
