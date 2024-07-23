from .helpers import get_attacking_moves, get_non_attacking_moves
from .move import Move
from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector


class Board:
    def __init__(self, pieces: dict[Vector, Piece]) -> None:
        self.__pieces = {**pieces}
        self.__move_history: list[Move] = []

    @property
    def __occupied_squares(self) -> list[Vector]:
        return list(self.__pieces.keys())

    def try_get_piece(self, coordinates: Vector) -> Piece | None:
        return self.__pieces.get(coordinates)

    def get_piece(self, coordinates: Vector) -> Piece:
        piece = self.try_get_piece(coordinates)

        if piece is None:
            raise ValueError(f"No piece found for coordinates: {coordinates}")

        return piece

    def move(self, move: Move):
        # TODO - add move validation

        for movement in move.movements:
            self.__pieces.pop(movement.attack_location, None)
            self.__pieces[movement.destination] = self.__pieces.pop(movement.origin)

        self.__move_history.append(move)

    def promote(self, coordinates: Vector, new_type: PieceType) -> None:
        color = self.get_piece(coordinates).color

        self.__pieces[coordinates] = Piece(new_type, color)

    # TODO - maybe get_pieces with condition passed
    # although pieces is accessible, so might not be useful
    def __get_king_location(self, color: Color) -> Vector | None:
        king_location = only(
            (
                coordinates
                for coordinates, piece in self.__pieces.items()
                if piece.type == PieceType.King and piece.color == color
            ),
            f"More than one king on {color.name} team",
        )

        # if king is None:
        #     raise ValueError(f"No king found for {color} team")

        return king_location

    def piece_at_square_has_moved(self, square: Vector) -> bool:
        self.get_piece(square)

        return any(move.destination == square for move in self.__move_history)

    def get_last_move(self) -> Move | None:
        return last(self.__move_history)

    def get_possible_moves(self, square: Vector) -> list[Move]:
        return [
            move
            for move in self.__get_unobstructed_moves(square)
            if not self.__will_be_in_check_after_move(move)
        ]

    def __get_unobstructed_moves(self, square: Vector) -> list[Move]:
        return self.__get_attacking_moves(square) + self.__get_non_attacking_moves(
            square
        )

    def __get_attacking_moves(self, square: Vector) -> list[Move]:
        return get_attacking_moves(square, self)

    def __get_non_attacking_moves(self, square: Vector) -> list[Move]:
        return get_non_attacking_moves(square, self)

    def __will_be_in_check_after_move(self, move: Move) -> bool:
        board = Board(self.__pieces)
        color = board.get_piece(move.origin).color

        board.move(move)
        return board.in_check(color)

    def in_check(self, color: Color):
        return (
            coordinates := self.__get_king_location(color)
        ) is not None and self.square_attacked(coordinates, color)

    def square_attacked(self, square: Vector, color: Color) -> bool:
        return any(
            square
            in (
                move.attack_location
                for move in self.__get_attacking_moves(occupied_square)
            )
            for occupied_square in self.__occupied_squares
            if self.get_piece(occupied_square).color != color
        )

    def any_possible_moves(self, color: Color) -> bool:
        return any(
            any(self.get_possible_moves(square))
            for square in self.__occupied_squares
            if self.get_piece(square).color == color
        )
