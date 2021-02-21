
from __future__ import annotations
from coordinates import Coordinates
from repository import display_board
from board import Board
from player import Player


class Game:
    def __init__(self: Game) -> None:
        self.board = Board()
        self.__player = Player()

    def play(self: Game) -> None:

        while not self.over():
            self.__take_turn()
            self.__player.swap_color()

        # TODO - add ending message

        display_board(self.board)

    def __take_turn(self: Game) -> None:
        while True:
            display_board(self.board)
            print("%s's turn" % str(self.__player.color.name).capitalize())

            try:
                coordinates_to_move_from = Coordinates.get_coordinates("Enter which square to move from: ")
                piece_to_move = self.board.get_piece(coordinates_to_move_from)

                if not piece_to_move:
                    raise ValueError("No piece at %s" % Coordinates.convert_to_grid_value(coordinates_to_move_from))
                
                if piece_to_move.color != self.__player:
                    raise ValueError("You cannot move the opposing team's piece")

                print("\n" + "You have chosen: %s" % piece_to_move.symbol)
                
                coordinates_to_move_to = Coordinates.get_coordinates("Enter which square to move to: ")
                return self.board.evaluate_move(piece_to_move, coordinates_to_move_to)

            except ValueError as e:
                print("\n%s" % e)

    def over(self: Game) -> bool:
        return (self.board.check_mate(self.__player.color)
            or self.board.stale_mate(self.__player.color))
