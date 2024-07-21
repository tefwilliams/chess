from .board import Board, Move, get_starting_pieces, within_board
from .color import Color
from .display import BoardRenderer, BoardSquare
from .movement import MoveGenerator
from .piece import Piece, PieceType
from .shared import only
from .vector import Vector


class Game:
    def __init__(self) -> None:
        self.board = Board(get_starting_pieces())
        self.__movement = MoveGenerator(self.board)
        self.player_color = Color.White
        self.__display = BoardRenderer()
        self.__display.render_squares(self.board.pieces)

    def over(self) -> bool:
        return self.in_check_mate() or self.in_stale_mate()

    def in_check_mate(self) -> bool:
        return self.__movement.in_check(
            self.player_color
        ) and not self.__movement.any_possible_moves(self.player_color)

    def in_stale_mate(self) -> bool:
        return not self.__movement.in_check(
            self.player_color
        ) and not self.__movement.any_possible_moves(self.player_color)

    def take_turn(self) -> None:
        move = self.__get_move_selection()

        self.board.move(move)

        # TODO - check for promotion each turn using get_last_move
        if (
            last_piece_to_move := self.board.last_piece_to_move
        ) is not None and should_promote(last_piece_to_move):
            self.board.promote(last_piece_to_move, PieceType.Queen)

        self.swap_player()

    def swap_player(self) -> None:
        self.player_color = self.player_color.get_opposing_color()

    def __get_move_selection(self) -> Move:
        first_selection = None

        while True:
            self.__display.render_squares(
                self.board.get_last_move() or []
            )

            first_selection = (
                first_selection
                or self.__display.get_coordinate_selection(self.__is_valid_origin)
            )

            possible_moves = self.__movement.get_possible_moves(
                first_selection)

            self.__display.highlight(first_selection)
            self.__display.display_possible_moves(
                move.primary_movement.destination
                for move in possible_moves
            )

            second_selection = self.__display.get_coordinate_selection()

            if second_selection == first_selection:
                # Deselect square
                first_selection = None
                continue

            move = only(
                move
                for move in possible_moves
                if move.primary_movement.destination == second_selection
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
            and (piece := self.board.try_get_piece(coordinates)) is not None
            and piece.color == self.player_color
        )


def should_promote(piece: Piece):
    return piece.type == PieceType.Pawn and piece.coordinates.row == (
        7 if piece.color == Color.White else 0
    )
