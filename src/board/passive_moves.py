from .board import Board
from .helpers import (
    get_attacking_moves,
    get_non_attacking_moves,
    get_squares_until_blocked,
    non_attacking_square_blocked_callback,
    get_unit_step_forward,
)
from .move import Move, Movement
from ..color import Color
from ..piece import Piece, PieceType
from ..shared import only, last
from ..vector import Vector


class PassiveMoves:
    def __init__(self, board: Board) -> None:
        self.__board = board

    def get_moves(self, square: Vector):
        # TODO - can we move some of this onto pieces (the callbacks)
        pass

    # ------------- PAWN -------------

    def get_pawn_non_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for destination in get_squares_until_blocked(
                non_attacking_square_blocked_callback(self.__board, color),
                square,
                get_unit_step_forward(color),
                1 if self.__board.piece_at_square_has_moved(square) else 2,
            )
        ]

    def get_en_passant_moves(
        square: Vector, color: Color, board: "Board"
    ) -> list[Move]:
        return [
            move
            for step in (unit_step_left, unit_step_right)
            for destination in get_squares_until_blocked(
                non_attacking_square_blocked_callback(board, color),
                square,
                get_unit_step_forward(color) + step,
                1,
            )
            if valid_en_passant(
                move := Move(
                    Movement(
                        square, destination, destination + get_unit_step_backward(color)
                    )
                ),
                board,
            )
        ]


def valid_en_passant(move: Move, board: "Board"):
    return (
        # Destination is clear due to non_attacking_square_blocked_callback
        (attacker := board.get_piece(move.origin)).type == PieceType.Pawn
        and (
            (defender := board.try_get_piece(defender_location := move.attack_location))
            and defender.type == PieceType.Pawn
        )
        and attacker.color != defender.color
        # Defender is last piece to move
        and (last_move := board.get_last_move())
        and last_move.destination == defender_location
        # Defender just moved two rows
        and abs(last_move.origin.row - last_move.destination.row) == 2
    )
