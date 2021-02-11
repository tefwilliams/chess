
from player import Player
from coordinates import Coordinates
from square import Square


def generate_new_board() -> list[list[Square]]:
    board_dimensions = Coordinates((8, 8))
    board: list[list[Square]] = []

    for i in range(board_dimensions.y):
        row: list[Square] = []

        for j in range(board_dimensions.x):
            coordinates = Coordinates((i, j))
            row.append(Square(coordinates))

        board.append(row)

    return board

board = generate_new_board()

def display_board(board: list[list[Square]]) -> None:
    board_dimensions = Coordinates((8, 8))

    print("\n" + "  ", end = '')

    for i in range(board_dimensions.x):
        column_number = i + 1
        print("| %s " %column_number, end = '')

    print("| ")
    print_row_break(board_dimensions.x)

    for row in board:
        print("%s " %chr(65), end='')

        for square in row:
            print("| %s " %square.symbol, end='')

        print("| ")
        print_row_break(board_dimensions.x)

    print("\n")

def print_row_break(row_length: int):
    dashes_per_column = 4
    print("-" * (row_length + 1) * dashes_per_column)

def play(board):
    player_color = 'white'

    for i in range(1):
        move(player_color)

    swap_player(player_color)
    display_board(board)


def swap_player(player: Player) -> None:
    player = 'black' if player == 'white' else 'white'

def move(player: Player) -> None:
    display_board(board)

    print("%s's turn" %('White' if player == 'white' else 'Black'))

    move_from_coordinates = get_coordinates("Enter which square to move from: ")
    move_to_coordinates = get_coordinates("Enter which square to move to: ")


def get_coordinates(input_text: str) -> Coordinates:
    while True:
        try:
            coordinates = input(input_text).upper()

            if not are_valid_coordinates(coordinates):
                raise ValueError("Invalid coordinates")

            coordinates_as_indices = format_coordinates(coordinates)
            return Coordinates(coordinates_as_indices)

        except ValueError as e:
            print(e)

def are_valid_coordinates(coordinates: str) -> bool:
    if len(coordinates) != 2:
        return False

    if coordinates[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        return False

    if coordinates[1] not in ['1', '2', '3', '4', '5', '6', '7', '8']:
        return False

    return True
            
def format_coordinates(coordinates: str) -> tuple[int, int]:
    y_grid_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    x_grid_values = ['1', '2', '3', '4', '5', '6', '7', '8']

    return (y_grid_values.index(coordinates[0]), x_grid_values.index(coordinates[1]))

