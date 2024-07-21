from .move import Move
from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector


class Board:
    def __init__(self, pieces: dict[Vector, Piece]) -> None:
        self.__pieces: dict[Vector, Piece] = pieces
        self.__move_history = []

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
            self.__pieces.pop(movement.attack_location)

            self.__pieces[movement.destination] = self.__pieces.pop(
                movement.origin)

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

    def get_last_move(self) -> Move | None:
        return last(self.__move_history)
