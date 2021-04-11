board_size = 8

row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
column_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

board_edge_thickness = 20  # px
board_border_thickness = 5  # px
square_size = 60  # px

white, black, brown, light_brown = (
    255, 255, 255), (0, 0, 0), (101, 67, 33), (187, 128, 65)

green = (118, 150, 86)
light_green = (186, 202, 43)

cream = (238, 238, 210)
yellow = (246, 246, 105)

display_size = board_edge_thickness * 2 + \
    board_border_thickness * 4 + square_size * board_size
