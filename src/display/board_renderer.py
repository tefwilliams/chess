import os
import pygame
from math import floor
from typing import Callable, Iterable
from .variables import (
    display_size,
    gray,
    cream,
    yellow,
    green,
    light_green,
    brown,
    light_brown,
    board_edge_thickness,
    board_border_thickness,
    square_size,
)
from ..board import Board
from ..piece import Piece
from ..vector import Vector


script_dir = os.path.dirname(__file__)
icons_folder_path = os.path.join(script_dir, "../../icons")


class BoardRenderer:
    def __init__(self, board: Board) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((display_size, display_size))
        self.screen.fill(brown)

        self.__board = board

        pygame.display.set_caption("Chess")
        pygame.display.set_icon(
            pygame.image.load(f"{icons_folder_path}/game_favicon.png")
        )

        self.__render_board_edge()

    def get_coordinate_selection(
        self, can_select: Callable[[Vector], bool] = lambda _: True
    ) -> Vector:
        while True:
            coordinates = self.__get_coordinates_from_mouse_position()

            pygame.mouse.set_system_cursor(
                pygame.SYSTEM_CURSOR_HAND
                if can_select(coordinates)
                else pygame.SYSTEM_CURSOR_ARROW
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONUP and can_select(coordinates):
                    return coordinates

    def __get_coordinates_from_mouse_position(self):
        return Vector(
            *(
                floor(
                    (coord - board_edge_thickness - board_border_thickness * 2)
                    / square_size
                )
                # get_pos returns (x, y)
                for coord in pygame.mouse.get_pos()
            )
        )

    def __render_board_edge(self) -> None:
        outer_margin = board_border_thickness
        outer_size = display_size - outer_margin * 2

        pygame.draw.rect(
            self.screen,
            light_brown,
            [outer_margin, outer_margin, outer_size, outer_size],
        )

        inner_margin = board_border_thickness + board_edge_thickness
        inner_size = display_size - inner_margin * 2

        pygame.draw.rect(
            self.screen, brown, [inner_margin, inner_margin, inner_size, inner_size]
        )

        pygame.display.update()

    # TODO - maybe make highlight a separate method
    def render_squares(
        self, squares_to_highlight: Iterable[Vector] | None = None
    ) -> None:
        for row_number in range(Board.size):
            for column_number in range(Board.size):
                square = Vector(column_number, row_number)

                self.__render_square(
                    square,
                    square in (squares_to_highlight or []),
                )

        pygame.display.update()

    def __render_square(self, square: Vector, highlighted: bool = False):
        odd_color, even_color = (yellow, light_green) if highlighted else (cream, green)
        square_color = odd_color if (square.col + square.row) % 2 == 0 else even_color

        top_left = get_square_location(square)

        pygame.draw.rect(
            self.screen,
            square_color,
            (top_left.col, top_left.row, square_size, square_size),
        )

        if piece := self.__board.try_get_piece(square):
            self.__display_piece(piece, square)

    def highlight(self, square: Vector):
        self.__render_square(square, True)
        pygame.display.update()

    def __display_piece(self, piece: Piece, coordinates: Vector) -> None:
        piece_icon = pygame.image.load(
            f"{icons_folder_path}/{piece.color.name}_{piece.type.name}.png"
        )

        icon_rect = piece_icon.get_rect()
        icon_width = icon_rect.width
        icon_height = icon_rect.height

        aspect_ratio = icon_width / icon_height

        icon_height = round(square_size * 0.8)
        icon_width = round(aspect_ratio * icon_height)

        top_left = get_square_location(coordinates) + Vector(
            (square_size - icon_width) // 2, (square_size - icon_height) // 2
        )

        scaled_piece_icon = pygame.transform.scale(
            piece_icon, (icon_width, icon_height)
        )
        self.screen.blit(scaled_piece_icon, [top_left.col, top_left.row])

    def display_possible_moves(self, squares: Iterable[Vector]) -> None:
        for square in squares:
            has_piece = self.__board.try_get_piece(square) is not None

            square_location = get_square_location(square, True)

            pygame.draw.circle(
                self.screen,
                gray,
                center=[square_location.col, square_location.row],
                radius=round(square_size * 0.4 if has_piece else square_size * 0.2),
                width=round(square_size * 0.1 if has_piece else 0),
            )

        pygame.display.update()


def get_square_location(square: Vector, center=False) -> Vector:
    board_margin = board_border_thickness * 2 + board_edge_thickness
    top_left = square * square_size + board_margin

    return top_left + square_size // 2 if center else top_left
