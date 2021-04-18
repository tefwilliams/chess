
from ..player import Color
from ..coordinates import Coordinates


class Movement:
    @staticmethod
    def get_diagonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        diagonal_squares: list[list[Coordinates]] = []

        directions = [(y, x) for y in [-1, 1] for x in [-1, 1]]

        for direction in directions:
            squares_in_direction = Movement.__get_squares_in_direction(
                origin_coordinates, direction)
            diagonal_squares.append(squares_in_direction)

        return diagonal_squares

    @staticmethod
    def get_orthogonal_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        orthogonal_squares: list[list[Coordinates]] = []

        directions = [(y, x) for y in [-1, 0, 1]
                      for x in [-1, 0, 1] if abs(y + x) == 1]

        for direction in directions:
            squares_in_direction = Movement.__get_squares_in_direction(
                origin_coordinates, direction)
            orthogonal_squares.append(squares_in_direction)

        return orthogonal_squares

    @staticmethod
    def get_adjacent_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        adjacent_squares: list[list[Coordinates]] = []

        directions = [(y, x) for y in [-1, 0, 1]
                      for x in [-1, 0, 1] if not y == x == 0]

        for direction in directions:
            squares_in_direction = Movement.__get_squares_in_direction(
                origin_coordinates, direction, 1)
            adjacent_squares.append(squares_in_direction)

        return adjacent_squares

    @staticmethod
    def get_knight_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        knight_squares: list[list[Coordinates]] = []

        directions = [(y, x) for y in [-2, -1, 1, 2]
                      for x in [-2, -1, 1, 2] if not abs(y) == abs(x)]

        for direction in directions:
            squares_in_direction = Movement.__get_squares_in_direction(
                origin_coordinates, direction, 1)
            knight_squares.append(squares_in_direction)

        return knight_squares

    @staticmethod
    def get_castle_squares(origin_coordinates: Coordinates) -> list[list[Coordinates]]:
        castle_squares: list[list[Coordinates]] = []

        directions = [(0, x) for x in [-1, 1]]

        for direction in directions:
            castle_squares.append(Movement.__get_squares_in_direction(
                origin_coordinates, direction))

        return castle_squares

    @staticmethod
    def get_pawn_squares(origin_coordinates: Coordinates, color: Color, has_moved: bool) -> list[list[Coordinates]]:
        direction = color.get_step_forward()

        if not has_moved:
            return [Movement.__get_squares_in_direction(origin_coordinates, direction, 2)]

        return [Movement.__get_squares_in_direction(origin_coordinates, direction, 1)]

    @staticmethod
    def get_pawn_attack_squares(origin_coordinates: Coordinates, color: Color) -> list[list[Coordinates]]:
        pawn_squares: list[list[Coordinates]] = []

        y = color.get_step_forward()[0]
        directions = [(y, x) for x in [-1, 1]]

        for direction in directions:
            squares_in_direction = Movement.__get_squares_in_direction(
                origin_coordinates, direction, 1)
            pawn_squares.append(squares_in_direction)

        return pawn_squares

    @staticmethod
    def __get_squares_in_direction(coordinates: Coordinates, step_in_direction: tuple[int, int], number_of_steps: int = None) -> list[Coordinates]:
        squares_in_direction: list[Coordinates] = []
        square_in_direction = coordinates

        if number_of_steps:
            for i in range(number_of_steps):
                square_in_direction = square_in_direction.move_by(
                    step_in_direction)
                squares_in_direction.append(square_in_direction)

        else:
            while square_in_direction.within_board:
                square_in_direction = square_in_direction.move_by(
                    step_in_direction)
                squares_in_direction.append(square_in_direction)

        return list(filter(lambda square: square.within_board, squares_in_direction))
