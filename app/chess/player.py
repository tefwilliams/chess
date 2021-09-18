
from __future__ import annotations
from enum import Enum


class Player:
    def __init__(self: Player):
        self.__color = Color.white

    @property
    def color(self: Player) -> Color:
        return self.__color

    def swap_color(self: Player) -> None:
        self.__color = self.__color.get_opposing_color()


# TODO - pull class into new file
class Color(Enum):
    white = 0
    black = 1

    def get_opposing_color(self: Color) -> Color:
        return Color.white if self == Color.black else Color.black

    def get_step_forward(self: Color) -> tuple[int, int]:
        return (1, 0) if self == Color.white else (-1, 0)
