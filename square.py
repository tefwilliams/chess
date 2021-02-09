
from __future__ import annotations
from repository import PieceTypes
from coordinates import Coordinates
from typing import Union
from piece import Piece


class Square:
    def __init__(self: Square, coordinates: Coordinates) -> None:
        self.__coordinates = coordinates
        self.piece = self.__get_starting_piece()

    def __get_starting_piece(self: Square) -> Union[Piece, None]:
        if self.__coordinates.y in [1, 6]:
            return Piece(PieceTypes.pawn)

        if self.__coordinates.y in [0, 7]:
            if self.__coordinates.x in [0, 7]:
                return Piece(PieceTypes.rook)

            if self.__coordinates.x in [1, 6]:
                return Piece(PieceTypes.knight)

            if self.__coordinates.x in [2, 5]:
                return Piece(PieceTypes.bishop)

            if self.__coordinates.x == 3:
                return Piece(PieceTypes.queen)

            if self.__coordinates.x == 4:
                return Piece(PieceTypes.king)


    @property
    def coordinates(self: Square) -> tuple[int, int]:
        return self.__coordinates