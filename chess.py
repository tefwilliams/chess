

def generate_new_board() -> list[list[str]]:
    board_dimensions = [8, 8]
    board = [['empty'] * board_dimensions[1] * board_dimensions[0]]

    for i in range(board_dimensions[0]):
        for j in range(board_dimensions[1]):
