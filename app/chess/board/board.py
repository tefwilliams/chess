from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector

from ..movement import get_unit_step_backward


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

    def move(self, piece: Piece, destination: Vector) -> None:
        # TODO - handle special moves
        # (castle, promotion, en passant)
        piece_to_take = self.try_get_piece(destination)

        if piece_to_take:
            self.pieces.remove(piece_to_take)

        piece.move(destination)
        self.__moved_pieces.append(piece)

    def castle(self, king: Piece, destination: Vector) -> None:
        moving_left = king.coordinates.col > destination.col

        rook_coordinates = Vector(king.coordinates.row, 0 if moving_left else 7)
        rook = self.get_piece(rook_coordinates)
        rook_destination = Vector(
            destination.row, destination.col + (1 if moving_left else -1)
        )

        king.move(destination)
        rook.move(rook_destination)
        # TODO - should record this in some way

    def en_passant(self, pawn: Piece, destination: Vector) -> None:
        piece_to_take = self.get_piece(destination + get_unit_step_backward(pawn.color))
        self.pieces.remove(piece_to_take)

        pawn.move(destination)
        # TODO - how do we tell this is en passant?
        self.__moved_pieces.append(pawn)

    def promote(self, pawn: Piece, new_type: PieceType) -> None:
        pawn.type = new_type

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
