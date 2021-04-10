
from __future__ import annotations
import pygame


class Screen:
    board_size = 8

    board_edge_thickness = 30  # px
    board_border_thickness = 5  # px

    square_size = 60  # px

    white, black, brown = (255, 255, 255), (0, 0, 0), (187, 129, 65)

    size = board_edge_thickness * 2 + \
        board_border_thickness * 4 + square_size * board_size

    def __init__(self: Screen) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((Screen.size, Screen.size))
        self.screen.fill(Screen.black)

        self.__create_board_edge()

        self.font = pygame.font.SysFont('Arial', 25)

        pygame.display.set_caption("Chess")

        icon = pygame.image.load("icons/game_icon.png")
        pygame.display.set_icon(icon)

        [self.__create_square(row_number, column_number)
         for row_number in range(Screen.board_size) for column_number in range(Screen.board_size)]

        self.__label_columns()
        self.__label_rows()

        pygame.display.update()

    def __create_board_edge(self: Screen) -> None:
        outer_margin = Screen.board_border_thickness
        outer_size = Screen.size - outer_margin * 2

        pygame.draw.rect(self.screen, Screen.white, [
                         outer_margin, outer_margin, outer_size, outer_size])

        inner_margin = Screen.board_border_thickness + Screen.board_edge_thickness
        inner_size = Screen.size - inner_margin * 2

        pygame.draw.rect(self.screen, Screen.black, [
            inner_margin, inner_margin, inner_size, inner_size])

    def __create_square(self: Screen, row_number: int, column_number: int) -> None:
        square_color = Screen.white if (
            row_number + column_number) % 2 == 0 else Screen.black

        pygame.draw.rect(self.screen, square_color,
                         self.__get_square_parameters(row_number, column_number))

    def __get_square_parameters(self: Screen, row_number: int, column_number: int) -> tuple[int, int, int, int]:
        board_margin = Screen.board_border_thickness * 2 + Screen.board_edge_thickness

        left_margin = board_margin + Screen.square_size * column_number
        top_margin = board_margin + Screen.square_size * row_number

        return (left_margin, top_margin, Screen.square_size, Screen.square_size)

    def __label_columns(self: Screen) -> None:
        board_margin = Screen.board_border_thickness * 2 + Screen.board_edge_thickness
        column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for column_number in range(Screen.board_size):
            column_label = column_labels[column_number]

            text = self.font.render(
                column_label, True, Screen.black)

            text_width = text.get_rect().width  # TODO - consider calling get_rect() once
            text_height = text.get_rect().height

            left_margin = board_margin + \
                Screen.square_size * column_number + \
                (Screen.square_size - text_width) / 2

            top_margin = (board_margin - text_height) / 2

            bottom_margin = board_margin + \
                Screen.square_size * Screen.board_size + \
                top_margin  # TODO - consider naming of right_margin (not actually right margin)

            self.screen.blit(text, (left_margin, top_margin))
            self.screen.blit(text, (left_margin, bottom_margin))

    def __label_rows(self: Screen) -> None:
        board_margin = Screen.board_border_thickness * 2 + Screen.board_edge_thickness
        row_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

        for row_number in range(Screen.board_size):
            column_label = row_labels[row_number]

            text = self.font.render(
                column_label, True, Screen.black)

            text_width = text.get_rect().width  # TODO - consider calling get_rect() once
            text_height = text.get_rect().height

            left_margin = (board_margin - text_width) / 2

            right_margin = board_margin + \
                Screen.square_size * Screen.board_size + \
                left_margin  # TODO - consider naming of right_margin (not actually right margin)

            top_margin = board_margin + \
                Screen.square_size * row_number + \
                (Screen.square_size - text_height) / 2

            self.screen.blit(text, (left_margin, top_margin))
            self.screen.blit(text, (right_margin, top_margin))


Screen()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

pygame.quit()
quit()
