
from __future__ import annotations
from repository import PieceTypes


class Piece:
    def __init__(self: Piece, type: PieceTypes) -> None:
        self.__type = type

    @property
    def type(self: Piece) -> PieceTypes:
        return self.__type