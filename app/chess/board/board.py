from copy import deepcopy
from typing import Callable

from .move import Move
from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector


class Board:
    def __init__(self, pieces: set[Piece]) -> None:
        self.pieces = pieces
        self.last_piece_to_move: Piece | None = None

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

    def move(self, move: Move) -> Callable[[], None]:
        current_pieces = deepcopy(self.pieces)
        last_piece_to_move = deepcopy(self.last_piece_to_move)

        def revert_move():
            self.pieces = current_pieces
            self.last_piece_to_move = last_piece_to_move

        for movement in move:
            piece_to_take = self.try_get_piece(movement.attack_location)

            if piece_to_take:
                self.pieces.remove(piece_to_take)

            movement.piece.move(movement.destination)

        self.last_piece_to_move = move.primary_movement.piece
        return revert_move

    def promote(self, pawn: Piece, new_type: PieceType) -> None:
        pawn.type = new_type

    # TODO - maybe get_pieces with condition passed
    # although pieces is accessible, so might not be useful
    def get_king(self, color: Color) -> Piece:
        king = only(
            (
                piece
                for piece in self.pieces
                if piece.type == PieceType.King and piece.color == color
            ),
            f"More than one king on {color.name} team",
        )

        if king is None:
            raise ValueError(f"No king found for {color} team")

        return king

    def get_last_move(self) -> tuple[Vector, Vector] | None:
        return (
            (previous_coordinates, last_piece_to_move.coordinates)
            if (last_piece_to_move := self.last_piece_to_move)
            and (previous_coordinates := last(last_piece_to_move.coordinates_history))
            else None
        )
