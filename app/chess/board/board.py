from ..vector import Vector
from ..shared import only, last
from ..color import Color
from ..piece import Piece, PieceType
from ..movement import Move


class Board:
    def __init__(self, pieces: set[Piece]) -> None:
        self.pieces = pieces
        self.__moved_pieces: list[Piece] = []

    def try_get_piece(self, coordinates: Vector) -> Piece | None:
        return only(
            (piece for piece in self.pieces if piece.coordinates == coordinates),
            f"More than one piece with coordinates: {coordinates}",
        )

    def get_piece(self, coordinates: Vector) -> Piece:
        piece = self.try_get_piece(coordinates)

        if piece is None:
            raise ValueError(f"No piece found for coordinates: {coordinates}")

        return piece

    def move(self, move: Move) -> None:
        # TODO - handle special moves
        # (castle, promotion, en passant)
        piece_to_take = self.try_get_piece(move.destination)

        if piece_to_take:
            self.pieces.remove(piece_to_take)

        move.piece.move(move.destination)
        self.__moved_pieces.append(move.piece)

    def revert_last_move(self):
        raise NotImplementedError()

    # TODO - maybe get_pieces with condition passed
    # although pieces is accessible, so might not be useful
    def get_king(self, color: Color) -> Piece | None:
        return only(
            (
                piece
                for piece in self.pieces
                if piece.type == PieceType.King and piece.color == color
            ),
            f"More than one king on {color.name} team",
        )

    @property
    def last_piece_to_move(self):
        return last(self.__moved_pieces)

    def get_last_move(self) -> tuple[Vector, Vector] | None:
        return (
            (previous_coordinates, last_piece_to_move.coordinates)
            if (last_piece_to_move := self.last_piece_to_move)
            and (previous_coordinates := last(last_piece_to_move.coordinates_history))
            else None
        )
