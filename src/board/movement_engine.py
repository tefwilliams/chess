from .aggressive_moves import AggressiveMoves
from .board import Board
from .move import Move
from .passive_moves import PassiveMoves
from ..color import Color
from ..piece import PieceType
from ..shared import only
from ..vector import Vector


class MovementEngine:
    def __init__(self, board: Board) -> None:
        self.__board = board
        self.__aggressive_move_generator = AggressiveMoves(board)
        self.__passive_move_generator = PassiveMoves(
            board, self.__aggressive_move_generator
        )

    def get_possible_moves(self, square: Vector) -> list[Move]:
        return [
            move
            for move in (
                self.__aggressive_move_generator.get_moves(square)
                + self.__passive_move_generator.get_moves(square)
            )
            if not self.__will_be_in_check_after_move(move)
        ]

    def __will_be_in_check_after_move(self, move: Move) -> bool:
        board = Board(self.__board.pieces)
        movement_engine = MovementEngine(board)

        color = board.get_piece(move.origin).color
        board.move(move)

        return movement_engine.in_check(color)

    def in_check(self, color: Color) -> bool:
        king_location = only(
            square
            for square, piece in self.__board.pieces.items()
            if piece.type == PieceType.King and piece.color == color
        )

        return (
            king_location is not None
            and self.__aggressive_move_generator.square_attacked(king_location, color)
        )

    def any_possible_moves(self, color: Color) -> bool:
        return any(
            move
            for square in self.__board.pieces
            if self.__board.get_piece(square).color == color
            for move in self.get_possible_moves(square)
        )
