from enum import Enum


class Color(Enum):
    White = 0
    Black = 1

    def get_opposing_color(self):
        return Color.White if self == Color.Black else Color.Black
