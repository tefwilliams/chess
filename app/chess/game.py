from .helpers import within_board
from .board_renderer import BoardRenderer, BoardSquare
from .vector import Vector
from .repository import get_starting_pieces
from .board import Board
from .move import Move
from .color import Color


class Game:
    def __init__(self) -> None:
        self.board = Board(get_starting_pieces())
        self.__current_color = Color.White
        self.__display = BoardRenderer()
        self.__display.render_squares(self.board.pieces)

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
            self.__display.render_squares(
                self.board.pieces, self.board.get_last_move() or []
            )
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
        origin = self.__display.get_coordinate_selection(
            self.__is_valid_origin, handle_quit
        )

        selected_piece = self.board.get_piece(origin)

        self.__display.highlight(BoardSquare(origin, selected_piece))
        self.__display.display_possible_moves(
            BoardSquare(coordinates, self.board.try_get_piece(coordinates))
            for coordinates in self.board.get_possible_moves(selected_piece)
        )

        destination = self.__display.get_coordinate_selection(
            lambda coordinate: self.__is_valid_destination(coordinate, origin),
            handle_quit,
        )

        return Move(selected_piece, destination)

    def __is_valid_origin(self, coordinates: Vector):
        return (
            within_board(coordinates)
            and (piece := self.board.try_get_piece(coordinates)) is not None
            and piece.color == self.player_color
        )

    def __is_valid_destination(self, coordinates: Vector, origin: Vector):
        return (
            within_board(coordinates)
            and coordinates != origin
            and (
                (piece := self.board.try_get_piece(coordinates)) is None
                or piece.color != self.__current_color
            )
        )


def handle_quit():
    quit()
