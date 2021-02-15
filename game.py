
from __future__ import annotations
from coordinates import Coordinates
from repository import display_board
from board import Board
from player import Player


class Game:
    __player: Player

    def __init__(self: Game) -> None:
        self.board = Board()
        self.__player = Player.white

    def play(self: Game) -> None:

        while not self.over():
            self.__take_turn()
            self.__swap_player()

        display_board(self.board)

    def __take_turn(self: Game) -> None:
        while True:
            display_board(self.board)
            print("%s's turn" % ('White' if self.__player == Player.white else 'Black'))

            try:
                coordinates_to_move_from = Coordinates.get_coordinates("Enter which square to move from: ")
                piece_to_move = self.board.get_piece(coordinates_to_move_from)

                if not piece_to_move:
                    raise ValueError("No piece at %s" % Coordinates.convert_to_grid_value(coordinates_to_move_from))
                
                if piece_to_move.player != self.__player:
                    raise ValueError("You cannot move the opposing team's piece")
                
                coordinates_to_move_to = Coordinates.get_coordinates("Enter which square to move to: ")
                return self.board.evaluate_move(self.__player, piece_to_move, coordinates_to_move_to)

            except ValueError as e:
                print("\n%s" % e)

    def __swap_player(self: Game) -> None:
        self.__player = Player.black if self.__player == Player.white else Player.white

    def over(self: Game):
        return self.board.check_mate(self.__player)
