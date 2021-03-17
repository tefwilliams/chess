
from ...src.player import Color
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

        directions = [Direction((y, x)) for y in [-2, -1, 1, 2] for x in [-2, -1, 1, 2] if not abs(y) == abs(x)]

        for direction in directions:
            squares_in_direction = [direction.step(origin_coordinates)]
            knight_squares.append([square for square in squares_in_direction if square.within_board])

        return knight_squares

    @staticmethod
    def get_pawn_squares(origin_coordinates: Coordinates, color: Color, has_moved: bool) -> list[list[Coordinates]]:
        y = 1 if color == Color.white else -1

        direction = Direction((y, 0))

        adjacent_square_in_direction = direction.step(origin_coordinates)
        squares_in_direction = [adjacent_square_in_direction]

        if not has_moved:
            squares_in_direction.append((direction.step(adjacent_square_in_direction)))

        return [[square for square in squares_in_direction if square.within_board]]

    @staticmethod
    def get_pawn_attack_squares(origin_coordinates: Coordinates, color: Color) -> list[list[Coordinates]]:
        pawn_squares: list[list[Coordinates]] = []
        y = 1 if color == Color.white else -1

        directions = [Direction((y, x)) for x in [-1, 1]]

        for direction in directions:
            squares_in_direction = [direction.step(origin_coordinates)]
            pawn_squares.append([square for square in squares_in_direction if square.within_board])

        return pawn_squares
