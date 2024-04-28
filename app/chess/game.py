from .display import BoardRenderer, BoardSquare
from .vector import Vector
from .board import Board, get_starting_pieces, within_board
from .movement import Move
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
        first_selection = None

        while True:
            self.__display.render_squares(
                self.board.pieces, self.board.get_last_move() or []
            )

            first_selection = (
                first_selection
                or self.__display.get_coordinate_selection(self.__is_valid_origin)
            )

            selected_piece = self.board.get_piece(first_selection)
            possible_moves = self.board.get_possible_moves(selected_piece)

            self.__display.highlight(BoardSquare(first_selection, selected_piece))
            self.__display.display_possible_moves(
                BoardSquare(coordinates, self.board.try_get_piece(coordinates))
                for coordinates in possible_moves
            )

            second_selection = self.__display.get_coordinate_selection()

            if second_selection == first_selection:
                # Deselect piece
                first_selection = None
                continue

            if second_selection not in possible_moves:
                # Select new piece or deselect
                first_selection = (
                    second_selection
                    if self.__is_valid_origin(second_selection)
                    else None
                )
                continue

            return Move(selected_piece, second_selection)

    def __is_valid_origin(self, coordinates: Vector):
        return (
            within_board(coordinates)
            and (piece := self.board.try_get_piece(coordinates)) is not None
            and piece.color == self.player_color
        )
