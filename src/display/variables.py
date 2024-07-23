from ..board import board_size

board_edge_thickness = 20  # px
board_border_thickness = 5  # px
square_size = 60  # px

gray = (105, 105, 105)

brown = (101, 67, 33)
light_brown = (187, 128, 65)

green = (118, 150, 86)
light_green = (186, 202, 43)

cream = (238, 238, 210)
yellow = (246, 246, 105)

display_size = (
    board_edge_thickness * 2 + board_border_thickness * 4 + square_size * board_size
)
