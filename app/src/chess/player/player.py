
from __future__ import annotations
from enum import Enum


class Player:
    def __init__(self: Player):
        self.__color = Color.white

    @property
    def color(self: Player) -> Color:
        return self.__color

    def swap_color(self: Player) -> None:
        self.__color = self.get_opposing_color()

    def get_opposing_color(self: Player) -> Color:
        return Color.get_opposing_color(self.__color)


# TODO - pull class into new file
class Color(Enum):
    white = 0
    black = 1

    @staticmethod
    def get_opposing_color(color: Color) -> Color:
        return Color.white if color == Color.black else Color.black