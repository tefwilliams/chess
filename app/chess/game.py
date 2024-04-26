import os
from .board_renderer import BoardRenderer, BoardSquare
from .vector import Vector
from .repository import get_starting_pieces
from .board import Board
from .move import Move
from .color import Color


script_dir = os.path.dirname(__file__)
icons_folder_path = os.path.join(script_dir, "../icons")


class Game:
    def __init__(self) -> None:
        self.board = Board(get_starting_pieces())
        self.__current_color = Color.White
        self.__renderer = BoardRenderer()
        self.__renderer.render_squares(self.board.pieces)

    @property
    def player_color(self) -> Color:
        return self.__current_color

    def over(self) -> bool:
        return self.check_mate() or self.stale_mate()

    def check_mate(self) -> bool:
        return self.board.check_mate(self.player_color)

    def stale_mate(self) -> bool:
        return self.board.stale_mate(self.player_color)

    def take_turn(self) -> None:
        while True:
            move = self.__get_move_selection()

            try:
                self.board.move(move)

            except ValueError:
                continue

            else:
                self.swap_player()
                break

    def swap_player(self) -> None:
        self.__current_color = self.player_color.get_opposing_color()

    def __get_move_selection(self) -> Move:
        origin = self.__renderer.get_coordinate_selection(self.__is_valid_origin)

        if origin == "quit":
            raise NotImplementedError()

        selected_piece = self.board.get_piece(origin)

        self.__renderer.highlight(BoardSquare(origin, selected_piece))
        self.__renderer.display_possible_moves(
            BoardSquare(coordinates, self.board.try_get_piece(coordinates))
            for coordinates in self.board.get_possible_moves(selected_piece)
        )

        destination = self.__renderer.get_coordinate_selection(
            lambda coordinate: self.__is_valid_destination(coordinate, origin)
        )

        if destination == "quit":
            raise NotImplementedError()

        return Move(selected_piece, destination)

    def __is_valid_origin(self, coordinate: Vector):
        return (
            piece := self.board.get_piece(coordinate)
        ) is not None and piece.color == self.player_color

    def __is_valid_destination(self, coordinate: Vector, origin: Vector):
        return coordinate != origin and (
            (piece := self.board.try_get_piece(coordinate)) is None
            or piece.color != self.__current_color
        )
