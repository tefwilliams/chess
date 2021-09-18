
from __future__ import annotations
import os
import pygame
from .coordinates import Coordinates
from .repository import get_starting_pieces
from .board import Board
from .player import Player
from .pieces import Piece
from .data import display_size, gray, cream, yellow, green, light_green, brown, light_brown, board_size, board_edge_thickness, board_border_thickness, square_size


script_dir = os.path.dirname(__file__)
icons_folder_path = os.path.join(script_dir, "../icons")


class Game:
    def __init__(self: Game) -> None:
        self.board = Board(get_starting_pieces())
        self.__player = Player()
        self.__intialize_display()

    def __intialize_display(self: Game) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((display_size, display_size))
        # self.screen = pygame.Surface((display_size, display_size))
        # screen.blit(self.screen, (0, 0))
        self.screen.fill(brown)

        pygame.display.set_caption("Chess")

        icon = pygame.image.load(f"{icons_folder_path}/game_favicon.png")
        pygame.display.set_icon(icon)

        self.__create_board_edge()

    @property
    def player(self: Game) -> Player:
        return self.__player

    def over(self: Game) -> bool:
        return self.check_mate() or self.stale_mate()

    def check_mate(self: Game) -> bool:
        return self.board.check_mate(self.player.color)

    def stale_mate(self: Game) -> bool:
        return self.board.stale_mate(self.player.color)

    def take_turn(self: Game) -> None:
        while True:
            piece_at_origin, destination_coordinates = self.__get_move_selection()

            try:
                self.board.evaluate_move(
                    piece_at_origin, destination_coordinates)

            except ValueError:
                continue

            else:
                self.player.swap_color()
                break

    def __create_board_edge(self: Game) -> None:
        outer_margin = board_border_thickness
        outer_size = display_size - outer_margin * 2

        pygame.draw.rect(self.screen, light_brown, [
                         outer_margin, outer_margin, outer_size, outer_size])

        inner_margin = board_border_thickness + board_edge_thickness
        inner_size = display_size - inner_margin * 2

        pygame.draw.rect(self.screen, brown, [
            inner_margin, inner_margin, inner_size, inner_size])

    def __get_move_selection(self: Game, origin_coordinates: Coordinates = None) -> tuple[Piece, Coordinates]:
        self.__refresh_display()

        if not origin_coordinates:
            origin_coordinates = self.__wait_for_coordinate_selection()

        piece_at_origin = self.board.get_piece(origin_coordinates)

        if not piece_at_origin or piece_at_origin.color != self.__player.color:
            return self.__get_move_selection()

        self.__highlight_square(origin_coordinates)
        self.__display_possible_moves(
            self.board.get_legal_moves(piece_at_origin))

        destination_coordinates = self.__wait_for_coordinate_selection()

        if destination_coordinates == origin_coordinates:
            return self.__get_move_selection()

        piece_at_destination = self.board.get_piece(
            destination_coordinates)

        if piece_at_destination and piece_at_destination.color == self.player.color:
            return self.__get_move_selection(destination_coordinates)

        return piece_at_origin, destination_coordinates

    def __refresh_display(self: Game) -> None:
        self.__create_squares()

        # TODO - add highlighting for last move
        # if self.__last_move:
        #     [self.__highlight_square(coordinates)
        #      for coordinates in self.__last_move]

        pygame.display.update()

    # TODO - maybe put on Coordinates
    def __wait_for_coordinate_selection(self: Game) -> Coordinates:
        while True:
            coordinates = Coordinates.get_coordinates_from_mouse_position(
                *pygame.mouse.get_pos())

            self.__set_cursor(coordinates)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.quit()  # if put on coordinates maybe move this out of game?

                if event.type == pygame.MOUSEBUTTONUP and coordinates.within_board:
                    return coordinates

    def __display_possible_moves(self: Game, list_of_moves: list[Coordinates]) -> None:
        for move in list_of_moves:
            self.__display_possible_move(move)

        pygame.display.update()

    def __display_possible_move(self: Game, coordinates: Coordinates) -> None:
        center = self.__get_square_location(coordinates, True)
        piece_at_coordinates = self.board.get_piece(coordinates)

        width = round(square_size * 0.1 if piece_at_coordinates else 0)
        radius = round(
            square_size * 0.4 if piece_at_coordinates else square_size * 0.2)

        pygame.draw.circle(self.screen, gray,
                           center, radius, width)

    @ staticmethod
    def quit() -> None:
        pygame.quit()
        quit()

    def __set_cursor(self: Game, coordinates: Coordinates) -> None:
        piece_at_coordinates = self.board.get_piece(coordinates)

        if piece_at_coordinates and piece_at_coordinates.color == self.player.color:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def __highlight_square(self: Game, coordinates: Coordinates) -> None:
        self.__create_square(coordinates, True)
        pygame.display.update()

    def __create_squares(self: Game) -> None:
        for row_number in range(board_size):
            for column_number in range(board_size):
                self.__create_square(Coordinates((row_number, column_number)))

    def __create_square(self: Game, coordinates: Coordinates, highlighted: bool = False) -> None:
        square_color = cream if (
            coordinates.y + coordinates.x) % 2 == 0 else green

        if highlighted:
            square_color = yellow if (
                coordinates.y + coordinates.x) % 2 == 0 else light_green

        left_margin, top_margin = self.__get_square_location(coordinates)

        pygame.draw.rect(self.screen, square_color,
                         (left_margin, top_margin, square_size, square_size))

        piece_at_square = self.board.get_piece(coordinates)

        if piece_at_square:
            self.__display_piece(piece_at_square)

    def __get_square_location(self: Game, coordinates: Coordinates, center: bool = False) -> tuple[int, int]:
        board_margin = board_border_thickness * 2 + board_edge_thickness

        left_margin = board_margin + square_size * coordinates.x
        top_margin = board_margin + square_size * coordinates.y

        if center:
            return left_margin + square_size // 2, top_margin + square_size // 2

        return left_margin, top_margin

    def __display_piece(self: Game, piece: Piece) -> None:
        piece_icon = pygame.image.load(
            f'{icons_folder_path}/{piece.color.name}_{piece.type.name}.png')
        left_margin, top_margin = self.__get_square_location(
            piece.coordinates)

        icon_rect = piece_icon.get_rect()
        icon_width = icon_rect.width
        icon_height = icon_rect.height

        aspect_ratio = icon_width / icon_height

        icon_height = square_size * 0.8
        icon_width = aspect_ratio * icon_height

        left_margin += (square_size - icon_width) / 2
        top_margin += (square_size - icon_height) / 2

        scaled_piece_icon = pygame.transform.scale(
            piece_icon, (round(icon_width), round(icon_height)))
        self.screen.blit(scaled_piece_icon, (left_margin, top_margin))
