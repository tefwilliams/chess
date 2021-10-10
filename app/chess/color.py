
from __future__ import annotations
from enum import Enum
from .grid import Step, unit_step_down, unit_step_up


class Color(Enum):
    white = 0
    black = 1

    def get_opposing_color(self: Color) -> Color:
        return Color.white if self == Color.black else Color.black

    def get_step_forward(self: Color) -> Step:
        return unit_step_down if self == Color.white else unit_step_up
