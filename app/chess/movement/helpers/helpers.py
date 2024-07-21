from typing import Callable

from ...color import Color
from ...board import Board, within_board
from ...vector import Vector


# TODO - could move these to board?


def get_squares_until_blocked(
    square_blocked: Callable[[Vector, Vector | None], bool],
    start: Vector,
    step: Vector,
    max_number_steps: int | None = None,
) -> list[Vector]:
    current_square = start + step
    last_square = None
    squares: list[Vector] = []

    while (
        within_board(current_square)
        and not square_blocked(current_square, last_square)
        and not (max_number_steps is not None and len(squares) >= max_number_steps)
    ):
        squares.append(current_square)
        last_square = current_square
        current_square += step

    return squares


def attacking_square_blocked_callback(
    board: Board, color: Color
) -> Callable[[Vector, Vector | None], bool]:
    return lambda current_square, last_square: (
        friendly_piece_at_square(current_square, color, board)
        or (
            last_square is not None and enemy_piece_at_square(
                last_square, color, board)
        )
    )


def non_attacking_square_blocked_callback(
    board: Board, color: Color
) -> Callable[[Vector, Vector | None], bool]:
    return lambda current_square, _: (
        friendly_piece_at_square(current_square, color, board)
        or enemy_piece_at_square(current_square, color, board)
    )


def friendly_piece_at_square(square: Vector, color: Color, board: Board):
    return (piece := board.try_get_piece(square)) is not None and piece.color == color


def enemy_piece_at_square(square: Vector, color: Color, board: Board):
    return (piece := board.try_get_piece(square)) is not None and piece.color != color


def pawn_attacking_square_blocked_callback(
    board: Board, color: Color
) -> Callable[[Vector, Vector | None], bool]:
    return lambda current_square, last_square: (
        friendly_piece_at_square(current_square, color, board)
        or not enemy_piece_at_square(last_square, color, board)
    )
