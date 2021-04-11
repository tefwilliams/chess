board_size = 8

row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
column_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

board_edge_thickness = 40  # px
board_border_thickness = 5  # px
square_size = 60  # px

white, black, gray, yellow = (
    255, 255, 255), (0, 0, 0), (180, 180, 180), (255, 252, 187)

display_size = board_edge_thickness * 2 + \
    board_border_thickness * 4 + square_size * board_size
