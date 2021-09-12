
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ..player import Color

if TYPE_CHECKING:
    from ...chess.coordinates import Coordinates
    from ...chess.board import Board


class Piece:
    type: PieceTypes

    def __init__(self: Piece, coordinates: Coordinates, color: Color) -> None:
        self.__color = color
        self.__coordinates = coordinates
        # TODO - maybe make this a list of coordinates, since we can work out the moves from that
        # also need to record what turn a move was made on
        self.__positions: dict[int, Coordinates] = {}
        self.__moves: list[tuple[Coordinates, Coordinates]] = []

    @property
    def color(self: Piece) -> Color:
        return self.__color

    @property
    def coordinates(self: Piece) -> Coordinates:
        return self.__coordinates

    @property
    def previous_coordinates(self: Piece) -> Coordinates | None:
        if not self.has_moved:
            return None

        return self.__moves[-1][0]

    @property
    def has_moved(self: Piece) -> bool:
        return len(self.__moves) > 0

    def move(self: Piece, new_coordinates: Coordinates) -> None:
        self.__moves.append((self.coordinates, new_coordinates))
        self.__coordinates = new_coordinates

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        base_moves = self.get_base_moves(board)
        return board.get_legal_moves(self, base_moves)

    def get_base_moves(self: Piece, board: Board) -> list[list[Coordinates]]:
        raise NotImplementedError


class PieceTypes(Enum):
    king = 0
    queen = 1
    bishop = 2
    knight = 3
    rook = 4
    pawn = 5
