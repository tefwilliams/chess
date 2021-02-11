
from square import Square
from board import Board
from player import Player
from coordinates import Coordinates


board = Board()

def display_board(board: Board) -> None:
    board_dimensions = board.shape

    print("\n" + "  ", end = '')

    for i in range(board_dimensions.x):
        column_number = i + 1
        print("| %s " %column_number, end = '')

    print("| ")
    print_row_break(board_dimensions.x)

    for i, row in enumerate(board):
        print("%s " %chr(65 + i), end='')

        for square in row:
            print("| %s " %square.symbol, end='')

        print("| ")
        print_row_break(board_dimensions.x)

    print("\n")

def print_row_break(row_length: int):
    dashes_per_column = 4
    print("-" * (row_length + 1) * dashes_per_column)

def play(board: Board):
    player: Player = 'white'

    for i in range(1):
        take_turn(board, player)

    swap_player(player)
    display_board(board)

def swap_player(player: Player) -> None:
    player = 'black' if player == 'white' else 'white'

def take_turn(board: Board, player: Player) -> None:
    display_board(board)

    print("%s's turn" %('White' if player == 'white' else 'Black'))

    move_from_square = get_square("Enter which square to move from: ", board)
    move_to_square = get_square("Enter which square to move to: ", board)

    move_to_square.piece = move_from_square.piece
    move_from_square.piece = None


def get_square(input_text: str, board: Board) -> Square:
    while True:
        try:
            coordinates = input(input_text).upper()

            if not are_valid_coordinates(coordinates):
                raise ValueError("Invalid coordinates")

            y_coordinate, x_coordinate = format_coordinates(coordinates)
            return board[y_coordinate][x_coordinate]

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

    y_grid_values.reverse()

    return (y_grid_values.index(coordinates[0]), x_grid_values.index(coordinates[1]))

play(board)