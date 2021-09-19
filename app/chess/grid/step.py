
from __future__ import annotations
from .grid import Grid

class Step(Grid):

    @property
    def has_magnitude_one(self: Step) -> bool:
        return sum(self) == 1

unit_step_up = Step((-1, 0))
unit_step_right = Step((0, 1))
unit_step_down = Step((1, 0))
unit_step_left = Step((0, -1))

horizontal_unit_steps = [unit_step_right, unit_step_left]

vertical_unit_steps = [unit_step_up, unit_step_down]

orthogonal_unit_steps = horizontal_unit_steps + vertical_unit_steps

diagonal_unit_steps = [vertical_step + horizontal_step for vertical_step in vertical_unit_steps for horizontal_step in horizontal_unit_steps]

all_unit_steps = orthogonal_unit_steps + diagonal_unit_steps
