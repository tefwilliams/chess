
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
        self.__moves: list[tuple[Coordinates, Coordinates]] = []

    @property
    def color(self: Piece) -> Color:
        return self.__color

    @property
    def coordinates(self: Piece) -> Coordinates:
        return self.__coordinates

    @property
    def previous_coordinates(self: Piece) -> Coordinates:
        if not self.has_moved:
            return self.coordinates

        return self.__moves[-1][0]

    @property
    def has_moved(self: Piece) -> bool:
        return len(self.__moves) > 0

    @property
    def possible_moves(self: Piece) -> list[Coordinates]:
        return self.__possible_moves

    def move(self: Piece, coordinates: Coordinates) -> None:
        self.__moves.append((self.coordinates, coordinates))
        self.__coordinates = coordinates

    def update_possible_moves(self: Piece, board: Board) -> None:
        self.__possible_moves = self.get_possible_moves(board)

    def get_possible_moves(self: Piece, board: Board) -> list[Coordinates]:
        raise NotImplementedError

    def revert_last_move(self: Piece) -> None:
        self.__coordinates = self.previous_coordinates
        self.__moves.pop()

class PieceTypes(Enum):
    king = 0
    queen = 1
    bishop = 2
    knight = 3
    rook = 4
    pawn = 5
