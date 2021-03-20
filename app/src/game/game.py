
from __future__ import annotations
from ...src.coordinates import Coordinates
from ...src.repository import display_board, get_starting_pieces
from ...src.board import Board
from ...src.player import Player


class Game:
    def __init__(self: Game) -> None:
        self.board = Board(get_starting_pieces())
        self.__player = Player()

    @property
    def player(self: Game) -> Player:
        return self.__player

    def take_turn(self: Game) -> None:
        while True:
            display_board(self.board)
            print("%s's turn" % str(self.__player.color.name).capitalize())

            try:
                self.board.update_all_possible_moves()
                
                coordinates_to_move_from = Coordinates.get_coordinates("Enter which square to move from: ")
                piece_to_move = self.board.get_piece(coordinates_to_move_from)

                if not piece_to_move:
                    raise ValueError("No piece at %s" % Coordinates.convert_to_grid_value(coordinates_to_move_from))
                
                if piece_to_move.color != self.__player.color:
                    raise ValueError("You cannot move the opposing team's piece")

                print("\n" + "You have chosen: %s" % piece_to_move.symbol)
                
                coordinates_to_move_to = Coordinates.get_coordinates("Enter which square to move to: ")
                self.board.evaluate_move(piece_to_move, coordinates_to_move_to)

            except ValueError as e:
                print("\n%s" % e)

            else:
                break

    def over(self: Game) -> bool:
        return self.check_mate() or self.stale_mate()

    def check_mate(self: Game) -> bool:
        return self.board.check_mate(self.__player.color)

    def stale_mate(self: Game) -> bool:
        return self.board.stale_mate(self.__player.color)
