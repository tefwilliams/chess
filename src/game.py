from .board import Board, MovementEngine, Move, within_board
from .color import Color
from .display import BoardRenderer
from .piece import Piece, PieceType
from .shared import only
from .vector import Vector


class Game:
    def __init__(self, pieces: dict[Vector, Piece]) -> None:
        self.__board = Board(pieces)
        self.__movement_engine = MovementEngine(self.__board)

        self.player_color = Color.White
        self.__display = BoardRenderer(self.__board)
        self.__display.render_squares()

    def over(self) -> bool:
        return self.in_check_mate() or self.in_stale_mate()

    def in_check_mate(self) -> bool:
        return self.__movement_engine.in_check(
            self.player_color
        ) and not self.__movement_engine.any_possible_moves(self.player_color)

    def in_stale_mate(self) -> bool:
        return not self.__movement_engine.in_check(
            self.player_color
        ) and not self.__movement_engine.any_possible_moves(self.player_color)

    def take_turn(self) -> None:
        move = self.__get_move_selection()

        self.__board.move(move)

        # TODO - check for promotion each turn using get_last_move
        # This probably belongs on the board
        if should_promote(self.__board, desintation := move.destination):
            self.__board.promote(desintation, PieceType.Queen)

        self.swap_player()

    def swap_player(self) -> None:
        self.player_color = self.player_color.get_opposing_color()

    def __get_move_selection(self) -> Move:
        first_selection = None

        while True:
            self.__display.render_squares(
                (last_move := self.__board.last_move)
                and (
                    last_move.origin,
                    last_move.destination,
                )
            )

            first_selection = (
                first_selection
                or self.__display.get_coordinate_selection(self.__is_valid_origin)
            )

            possible_moves = self.__movement_engine.get_possible_moves(first_selection)

            self.__display.highlight(first_selection)
            self.__display.display_possible_moves(
                move.destination for move in possible_moves
            )

            second_selection = self.__display.get_coordinate_selection()

            if second_selection == first_selection:
                # Deselect square
                first_selection = None
                continue

            move = only(
                move for move in possible_moves if move.destination == second_selection
            )

            if not move:
                # Select new square or deselect
                first_selection = (
                    second_selection
                    if self.__is_valid_origin(second_selection)
                    else None
                )
                continue

            return move

    def __is_valid_origin(self, coordinates: Vector):
        return (
            within_board(coordinates)
            and (piece := self.__board.try_get_piece(coordinates)) is not None
            and piece.color == self.player_color
        )


def should_promote(board: Board, coordinates: Vector):
    # TODO - could potentially use board.last_move
    return (
        piece := board.get_piece(coordinates)
    ).type == PieceType.Pawn and coordinates.row == (
        0 if piece.color == Color.White else 7
    )
