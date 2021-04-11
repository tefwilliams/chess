
from __future__ import annotations
import pygame
from ..coordinates import Coordinates
from ..repository import display_board, get_starting_pieces
from ..board import Board
from ..player import Player
from ..pieces import Piece
from ..data import display_size, black, white, gray, board_size, board_edge_thickness, board_border_thickness, square_size


class Game:
    def __init__(self: Game) -> None:
        self.board = Board(get_starting_pieces())
        self.__player = Player()
        self.__intialize_display()

    def __intialize_display(self: Game) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((display_size, display_size))
        self.screen.fill(gray)

        self.text_font = pygame.font.SysFont('arial', 25)
        self.symbol_font = pygame.font.SysFont('segoeuisymbol', 40)

        pygame.display.set_caption("Chess")

        icon = pygame.image.load("icons/game_icon.png")
        pygame.display.set_icon(icon)

        self.__create_board_edge()
        self.__label_columns()
        self.__label_rows()

    @property
    def player(self: Game) -> Player:
        return self.__player

    def over(self: Game) -> bool:
        return self.check_mate() or self.stale_mate()

    def check_mate(self: Game) -> bool:
        return self.board.check_mate(self.__player.color)

    def stale_mate(self: Game) -> bool:
        return self.board.stale_mate(self.__player.color)

    def take_turn(self: Game) -> None:
        while True:
            try:
                origin_coordinates = self.__wait_for_coordinate_selection()
                piece_to_move = self.board.get_piece(origin_coordinates)

                if not piece_to_move:
                    raise ValueError("No piece at %s" % Coordinates.convert_to_grid_value(
                        origin_coordinates))

                if piece_to_move.color != self.__player.color:
                    raise ValueError(
                        "You cannot move the opposing team's piece")

                print("\n" + "You have chosen: %s" % piece_to_move.symbol)

                destination_coordinates = self.__wait_for_coordinate_selection()

                self.board.evaluate_move(
                    piece_to_move, destination_coordinates)

            except ValueError as e:
                print("\n%s" % e)

            else:
                break

    def __wait_for_coordinate_selection(self: Game) -> Coordinates:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    coordinates = Coordinates.get_coordinates_from_mouse_position(
                        *pygame.mouse.get_pos())

                    if coordinates and coordinates.within_board:
                        return coordinates

    def update_display(self: Game, board: Board) -> None:
        self.__create_empty_squares()

        for piece in board.pieces:
            self.__display_piece(piece)

        pygame.display.update()

    def __create_empty_squares(self: Game) -> None:
        [self.__create_empty_square(row_number, column_number)
         for row_number in range(board_size) for column_number in range(board_size)]

    def __create_board_edge(self: Game) -> None:
        outer_margin = board_border_thickness
        outer_size = display_size - outer_margin * 2

        pygame.draw.rect(self.screen, white, [
                         outer_margin, outer_margin, outer_size, outer_size])

        inner_margin = board_border_thickness + board_edge_thickness
        inner_size = display_size - inner_margin * 2

        pygame.draw.rect(self.screen, gray, [
            inner_margin, inner_margin, inner_size, inner_size])

    def __create_empty_square(self: Game, row_number: int, column_number: int) -> None:
        square_color = white if (
            row_number + column_number) % 2 == 0 else gray

        pygame.draw.rect(self.screen, square_color,
                         self.__get_square_parameters(row_number, column_number))

    def __get_square_parameters(self: Game, row_number: int, column_number: int) -> tuple[int, int, int, int]:
        board_margin = board_border_thickness * 2 + board_edge_thickness

        left_margin = board_margin + square_size * column_number
        top_margin = board_margin + square_size * row_number

        return (left_margin, top_margin, square_size, square_size)

    def __label_columns(self: Game) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for column_number in range(board_size):
            column_label = column_labels[column_number]

            text = self.text_font.render(
                column_label, True, black)

            # TODO - consider calling get_rect() once
            text_width = text.get_rect().width
            text_height = text.get_rect().height

            left_margin = board_margin + \
                square_size * column_number + \
                (square_size - text_width) / 2

            top_margin = (board_margin - text_height) / 2

            # TODO - consider naming of bottom_margin (not actually bottom margin)
            bottom_margin = board_margin + \
                square_size * board_size + \
                top_margin

            self.screen.blit(text, (left_margin, top_margin))
            self.screen.blit(text, (left_margin, bottom_margin))

    def __label_rows(self: Game) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        row_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

        for row_number in range(board_size):
            column_label = row_labels[row_number]

            text = self.text_font.render(
                column_label, True, black)

            # TODO - consider calling get_rect() once
            text_width = text.get_rect().width
            text_height = text.get_rect().height

            left_margin = (board_margin - text_width) / 2

            # TODO - consider naming of right_margin (not actually right margin)
            right_margin = board_margin + \
                square_size * board_size + \
                left_margin

            top_margin = board_margin + \
                square_size * row_number + \
                (square_size - text_height) / 2

            self.screen.blit(text, (left_margin, top_margin))
            self.screen.blit(text, (right_margin, top_margin))

    def __display_piece(self: Game, piece: Piece) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        row_number, column_number = piece.coordinates

        symbol = self.symbol_font.render(
            piece.symbol, True, black)

        # TODO - consider calling get_rect() once
        symbol_width = symbol.get_rect().width
        symbol_height = symbol.get_rect().height

        left_margin = board_margin + \
            square_size * column_number + \
            (square_size - symbol_width) / 2

        top_margin = board_margin + \
            square_size * row_number + \
            (square_size - symbol_height) / 2

        self.screen.blit(symbol, (left_margin, top_margin))
