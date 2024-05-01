from ...color import Color
from ...vector import Vector


unit_step_up = Vector(0, -1)
unit_step_right = Vector(1, 0)
unit_step_down = Vector(0, 1)
unit_step_left = Vector(-1, 0)

horizontal_unit_steps = (unit_step_right, unit_step_left)

vertical_unit_steps = (unit_step_up, unit_step_down)

orthogonal_unit_steps = horizontal_unit_steps + vertical_unit_steps

diagonal_unit_steps = tuple(
    vertical_step + horizontal_step
    for vertical_step in vertical_unit_steps
    for horizontal_step in horizontal_unit_steps
)


def get_unit_step_forward(color: Color):
    return unit_step_up if color == Color.White else unit_step_down


def get_unit_step_backward(color: Color):
    return get_unit_step_forward(color.get_opposing_color())
