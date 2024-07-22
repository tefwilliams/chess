from copy import deepcopy
from .helpers import get_attacking_moves, get_non_attacking_moves
from .move import Move
from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector


class Board:
    def __init__(self, pieces: dict[Vector, Piece]) -> None:
        self.__pieces: dict[Vector, Piece] = pieces
        self.__move_history: list[Move] = []

    @property
    def occupied_squares(self) -> list[Vector]:
        return list(self.__pieces.keys())

    def try_get_piece(self, coordinates: Vector) -> Piece | None:
        return self.__pieces.get(coordinates)

    def get_piece(self, coordinates: Vector) -> Piece:
        piece = self.try_get_piece(coordinates)

        if piece is None:
            raise ValueError(f"No piece found for coordinates: {coordinates}")

        return piece

    def move(self, move: Move):
        for movement in move:
            self.__pieces.pop(movement.attack_location, None)

            self.__pieces[movement.destination] = self.__pieces.pop(movement.origin)

        self.__move_history.append(move)

    def promote(self, coordinates: Vector, new_type: PieceType) -> None:
        # TODO - check that this isn't allowed
        # I should have to create a new piece and
        # assign it to these coordinates
        self.__pieces[coordinates].type = new_type

    # TODO - maybe get_pieces with condition passed
    # although pieces is accessible, so might not be useful
    def get_king_location(self, color: Color) -> Piece | None:
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

        return any(
            move.primary_movement.destination == square for move in self.__move_history
        )

    def get_last_move(self) -> Move | None:
        return last(self.__move_history)

    def get_possible_moves(self, square: Vector) -> list[Move]:
        return [
            move
            for move in self.get_unobstructed_moves(square)
            if not self.__will_be_in_check_after_move(move)
        ]

    def get_unobstructed_moves(self, square: Vector) -> list[Move]:
        return self.get_attacking_moves(square) + self.get_non_attacking_moves(square)

    def get_attacking_moves(self, square: Vector) -> list[Move]:
        return get_attacking_moves(square, self)

    def get_non_attacking_moves(self, square: Vector) -> list[Move]:
        return get_non_attacking_moves(square, self)

    def __will_be_in_check_after_move(self, move: Move) -> bool:
        test_board = deepcopy(self)
        color = test_board.get_piece(move.primary_movement.origin).color

        test_board.move(move)
        in_check = test_board.in_check(color)

        return in_check

    def in_check(self, color: Color):
        return (
            coordinates := self.get_king_location(color)
        ) is not None and self.square_attacked(coordinates, color)

    def square_attacked(self, square: Vector, color: Color) -> bool:
        return any(
            square
            in (
                move.primary_movement.attack_location
                for move in self.get_attacking_moves(occupied_square)
            )
            for occupied_square in self.occupied_squares
            if self.get_piece(occupied_square).color != color
        )

    def any_possible_moves(self, color: Color) -> bool:
        return any(
            any(self.get_possible_moves(square))
            for square in self.occupied_squares
            if self.get_piece(square).color == color
        )
