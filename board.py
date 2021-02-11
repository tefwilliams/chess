
from __future__ import annotations
from typing import Union
from coordinates import Coordinates
from square import Square


class Board(list[list[Square]]):
    def __init__(self: Board) -> None:
        self.__shape = Coordinates((8, 8))
        super().__init__(self.__generate())

    def __generate(self: Board) -> list[list[Square]]:
        board: list[list[Square]] = []

        for i in range(self.__shape.y):
            row: list[Square] = []

            for j in range(self.__shape.x):
                coordinates = Coordinates((i, j))
                row.append(Square(coordinates))

            board.append(row)

        return board

    def __getitem__(self: Board, coordinates: Union[int, Coordinates]):
        if type(coordinates) is int:
            return self[coordinates]

        if type(coordinates) is Coordinates:
            y, x = coordinates
            return self[y][x]

    @property
    def shape(self: Board) -> Coordinates:
        return self.__shape
