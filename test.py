
from __future__ import annotations
from chess import Board, Piece, board_size, board_edge_thickness, board_border_thickness, square_size
import pygame


class Screen:
    white, black, gray = (255, 255, 255), (0, 0, 0), (180, 180, 180)

    size = board_edge_thickness * 2 + \
        board_border_thickness * 4 + square_size * board_size

    def __init__(self: Screen) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((Screen.size, Screen.size))
        self.screen.fill(Screen.gray)

        self.__create_board_edge()

        self.text_font = pygame.font.SysFont('arial', 25)
        self.symbol_font = pygame.font.SysFont('segoeuisymbol', 40)

        pygame.display.set_caption("Chess")

        icon = pygame.image.load("icons/game_icon.png")
        pygame.display.set_icon(icon)

        self.__label_columns()
        self.__label_rows()

        self.__create_empty_squares()

        pygame.display.update()

    def should_exit(self: Screen) -> bool:
        return any(event.type == pygame.QUIT for event in pygame.event.get())

    def update(self: Screen, board: Board) -> None:
        self.__create_empty_squares()

        for piece in board.pieces:
            self.__display_piece(piece)

        pygame.display.update()

    def __create_empty_squares(self: Screen) -> None:
        [self.__create_empty_square(row_number, column_number)
         for row_number in range(board_size) for column_number in range(board_size)]

    def __create_board_edge(self: Screen) -> None:
        outer_margin = board_border_thickness
        outer_size = Screen.size - outer_margin * 2

        pygame.draw.rect(self.screen, Screen.white, [
                         outer_margin, outer_margin, outer_size, outer_size])

        inner_margin = board_border_thickness + board_edge_thickness
        inner_size = Screen.size - inner_margin * 2

        pygame.draw.rect(self.screen, Screen.gray, [
            inner_margin, inner_margin, inner_size, inner_size])

    def __create_empty_square(self: Screen, row_number: int, column_number: int) -> None:
        square_color = Screen.white if (
            row_number + column_number) % 2 == 0 else Screen.gray

        pygame.draw.rect(self.screen, square_color,
                         self.__get_square_parameters(row_number, column_number))

    def __get_square_parameters(self: Screen, row_number: int, column_number: int) -> tuple[int, int, int, int]:
        board_margin = board_border_thickness * 2 + board_edge_thickness

        left_margin = board_margin + square_size * column_number
        top_margin = board_margin + square_size * row_number

        return (left_margin, top_margin, square_size, square_size)

    def __label_columns(self: Screen) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for column_number in range(board_size):
            column_label = column_labels[column_number]

            text = self.text_font.render(
                column_label, True, Screen.black)

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

    def __label_rows(self: Screen) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        row_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

        for row_number in range(board_size):
            column_label = row_labels[row_number]

            text = self.text_font.render(
                column_label, True, Screen.black)

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

    def __display_piece(self: Screen, piece: Piece) -> None:
        board_margin = board_border_thickness * 2 + board_edge_thickness
        row_number, column_number = piece.coordinates

        symbol = self.symbol_font.render(
            piece.symbol, True, Screen.black)

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
