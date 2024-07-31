from .board import Board
from .helpers import (
    unit_step_left,
    unit_step_right,
    orthogonal_unit_steps,
    diagonal_unit_steps,
    get_squares_until_blocked,
    get_unit_step_forward,
    get_unit_step_backward,
    pawn_attacking_square_blocked_callback,
    attacking_square_blocked_callback,
    non_attacking_square_blocked_callback,
)
from .move import Move, Movement
from ..color import Color
from ..piece import PieceType
from ..vector import Vector


class AggressiveMoves:
    def __init__(self, board: Board) -> None:
        self.__board = board

    def get_moves(self, square: Vector):
        match (piece := self.__board.get_piece(square)).type:
            case PieceType.Pawn:
                return self.__get_pawn_attacking_moves(
                    square, piece.color
                ) + self.__get_en_passant_moves(square, piece.color)

            case PieceType.Rook:
                return self.__get_rook_attacking_moves(square, piece.color)

            case PieceType.Knight:
                return self.__get_knight_attacking_moves(square, piece.color)

            case PieceType.Bishop:
                return self.__get_bishop_attacking_moves(square, piece.color)

            case PieceType.Queen:
                return self.__get_queen_attacking_moves(square, piece.color)

            case PieceType.King:
                return self.__get_king_attacking_moves(square, piece.color)

    def square_attacked(self, square: Vector, color: Color) -> bool:
        return any(
            square == move.attack_location
            for occupied_square in self.__board.pieces
            if self.__board.get_piece(occupied_square).color != color
            for move in self.get_moves(occupied_square)
        )

    # ------------- PAWN -------------

    def __get_pawn_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in (unit_step_left, unit_step_right)
            for destination in get_squares_until_blocked(
                pawn_attacking_square_blocked_callback(self.__board, color),
                square,
                get_unit_step_forward(color) + step,
                1,
            )
        ]

    def __get_en_passant_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            move
            for step in (unit_step_left, unit_step_right)
            for destination in get_squares_until_blocked(
                non_attacking_square_blocked_callback(self.__board, color),
                square,
                get_unit_step_forward(color) + step,
                1,
            )
            if self.__valid_en_passant(
                move := Move(
                    Movement(
                        square, destination, destination + get_unit_step_backward(color)
                    )
                ),
            )
        ]

    # ------------- ROOK -------------

    def __get_rook_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in orthogonal_unit_steps
            for destination in get_squares_until_blocked(
                attacking_square_blocked_callback(self.__board, color),
                square,
                step,
            )
        ]

    # ------------- Knight -------------

    def __get_knight_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in (
                orthogonal_step + diagonal_step
                for orthogonal_step in orthogonal_unit_steps
                for diagonal_step in diagonal_unit_steps
            )
            if abs(step.row) + abs(step.col) == 3
            for destination in get_squares_until_blocked(
                attacking_square_blocked_callback(self.__board, color),
                square,
                step,
                1,
            )
        ]

    # ------------- Bishop -------------

    def __get_bishop_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in diagonal_unit_steps
            for destination in get_squares_until_blocked(
                attacking_square_blocked_callback(self.__board, color),
                square,
                step,
            )
        ]

    # ------------- Queen -------------

    def __get_queen_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in diagonal_unit_steps + orthogonal_unit_steps
            for destination in get_squares_until_blocked(
                attacking_square_blocked_callback(self.__board, color),
                square,
                step,
            )
        ]

    # ------------- King -------------

    def __get_king_attacking_moves(self, square: Vector, color: Color) -> list[Move]:
        return [
            Move(Movement(square, destination))
            for step in diagonal_unit_steps + orthogonal_unit_steps
            for destination in get_squares_until_blocked(
                attacking_square_blocked_callback(self.__board, color),
                square,
                step,
                1,
            )
        ]

    # ------------- Helpers -------------

    def __valid_en_passant(self, move: Move):
        return (
            # Destination is clear due to non_attacking_square_blocked_callback
            (attacker := self.__board.get_piece(move.origin)).type == PieceType.Pawn
            and (
                (
                    defender := self.__board.try_get_piece(
                        defender_location := move.attack_location
                    )
                )
                and defender.type == PieceType.Pawn
            )
            and attacker.color != defender.color
            # Defender is last piece to move
            and (last_move := self.__board.last_move)
            and last_move.destination == defender_location
            # Defender just moved two rows
            and abs(last_move.origin.row - last_move.destination.row) == 2
        )
