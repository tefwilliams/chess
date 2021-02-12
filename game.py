
from __future__ import annotations
from coordinates import Coordinates
from square import Square
from repository import display_board
from board import Board
from player import Player


class Game:
    def __init__(self: Game) -> None:
        self.board = Board()
        self.player: Player = 'white'

    def play(self: Game) -> None:

        for i in range(1):
            self.__take_turn()
            self.__swap_player()

        display_board(self.board)

    def __take_turn(self: Game) -> None:
        display_board(self.board)

        print("%s's turn" %('White' if self.player == 'white' else 'Black'))

        move_from_square = self.__get_square("Enter which square to move from: ")
        move_to_square = self.__get_square("Enter which square to move to: ")

        move_to_square.piece = move_from_square.piece
        move_from_square.piece = None

    def __get_square(self: Game, input_text: str) -> Square:
        while True:
            try:
                coordinates_as_string = input(input_text).upper()
                y_coordinate, x_coordinate = Coordinates.convert_to_coordinates(coordinates_as_string)

                return self.board[y_coordinate][x_coordinate]

            except ValueError as e:
                print(e)

    def __swap_player(self: Game) -> None:
        self.player = 'black' if self.player == 'white' else 'white'
