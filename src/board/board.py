from .move import Move
from ..piece import Piece, PieceType
from ..shared import last
from ..vector import Vector


class Board:
    # TODO - use this size parameter
    size = 8

    def __init__(self, pieces: dict[Vector, Piece]) -> None:
        self.__pieces = pieces.copy()
        self.__move_history: list[Move] = []

    @property
    def pieces(self) -> dict[Vector, Piece]:
        return self.__pieces.copy()

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

    def piece_at_square_has_moved(self, square: Vector) -> bool:
        self.get_piece(square)

        return any(move.destination == square for move in self.__move_history)

    @property
    def last_move(self) -> Move | None:
        return last(self.__move_history)
