
from __future__ import annotations
from pieces.king import King
from pieces.queen import Queen
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.piece import Piece
from coordinates import Coordinates
from typing import Union


class Square:
    def __init__(self: Square, coordinates: Coordinates) -> None:
        self.__coordinates = coordinates
        self.piece = self.__get_starting_piece()
        self.symbol = self.piece.symbol if self.piece else ' '

    def __get_starting_piece(self: Square) -> Union[Piece, None]:
        if self.__coordinates.y in [1, 6]:
            color = 'white' if self.__coordinates.y == 6 else 'black'
            return Pawn(color)

        if self.__coordinates.y in [0, 7]:
            color = 'white' if self.__coordinates.y == 7 else 'black'

            if self.__coordinates.x in [0, 7]:
                return Rook(color)

            if self.__coordinates.x in [1, 6]:
                return Knight(color)

            if self.__coordinates.x in [2, 5]:
                return Bishop(color)

            if self.__coordinates.x == 3:
                return Queen(color)

            if self.__coordinates.x == 4:
                return King(color)


    @property
    def coordinates(self: Square) -> tuple[int, int]:
        return self.__coordinates