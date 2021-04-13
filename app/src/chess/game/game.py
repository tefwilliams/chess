
from __future__ import annotations
import pygame
from ..coordinates import Coordinates
from ..repository import get_starting_pieces
from ..board import Board
from ..player import Player
from ..pieces import Piece
from ..data import display_size, black, white, cream, yellow, green, light_green, brown, light_brown, board_size, board_edge_thickness, board_border_thickness, square_size


class Game:
    def __init__(self: Game) -> None:
        self.board = Board(get_starting_pieces())
        self.__last_move: tuple[Coordinates, Coordinates]
        self.__player = Player()
        self.__intialize_display()

    def __intialize_display(self: Game) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((display_size, display_size))
        self.screen.fill(brown)

        self.font = pygame.font.SysFont('arial', 25)

        pygame.display.set_caption("Chess")

        icon = pygame.image.load("icons/game_favicon.png")
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
        origin_coordinates = None

        while True:
            self.__update_display()

            if not origin_coordinates:
                origin_coordinates = self.__wait_for_coordinate_selection()

            piece_at_origin = self.board.get_piece(origin_coordinates)

            if not piece_at_origin or piece_at_origin.color != self.__player.color:
                continue

            self.__highlight_square(origin_coordinates)

            destination_coordinates = self.__wait_for_coordinate_selection()

            if destination_coordinates == origin_coordinates:
                origin_coordinates = None
                continue

            piece_at_destination = self.board.get_piece(
                destination_coordinates)

            if piece_at_destination and piece_at_destination.color == self.player.color:
                origin_coordinates = destination_coordinates
                continue

            try:
                self.board.evaluate_move(
                    piece_at_origin, destination_coordinates)

            except ValueError as e:
                print("\n%s" % e)

            else:
                self.board.update_possible_moves()
                self.__last_move = (origin_coordinates,
                                    destination_coordinates)
                break

    @ staticmethod
    def quit() -> None:
        pygame.quit()
        quit()

    # TODO - maybe put on Coordinates
    def __wait_for_coordinate_selection(self: Game) -> Coordinates:
        while True:
            coordinates = Coordinates.get_coordinates_from_mouse_position(
                *pygame.mouse.get_pos())

            piece_at_coordinates = self.board.get_piece(coordinates)

            if piece_at_coordinates and piece_at_coordinates.color == self.player.color:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.quit()  # if put on coordinates maybe move this out of game?

                if event.type == pygame.MOUSEBUTTONUP and coordinates.within_board:
                    return coordinates

    def __highlight_square(self: Game, coordinates: Coordinates) -> None:
        self.__create_square(coordinates, True)
        pygame.display.update()

    def __update_display(self: Game) -> None:
        self.__create_squares()

        # TODO - add highlighting for last move
        # if self.__last_move:
        #     [self.__highlight_square(coordinates)
        #      for coordinates in self.__last_move]

        pygame.display.update()

    def __create_squares(self: Game) -> None:
        [self.__create_square(Coordinates((row_number, column_number)))
         for row_number in range(board_size) for column_number in range(board_size)]

    def __create_board_edge(self: Game) -> None:
        outer_margin = board_border_thickness
        outer_size = display_size - outer_margin * 2

        pygame.draw.rect(self.screen, light_brown, [
                         outer_margin, outer_margin, outer_size, outer_size])

        inner_margin = board_border_thickness + board_edge_thickness
        inner_size = display_size - inner_margin * 2

        pygame.draw.rect(self.screen, brown, [
            inner_margin, inner_margin, inner_size, inner_size])

    def __create_square(self: Game, coordinates: Coordinates, highlighted: bool = False) -> None:
        square_color = cream if (
            coordinates.y + coordinates.x) % 2 == 0 else green

        if highlighted:
            square_color = yellow if (
                coordinates.y + coordinates.x) % 2 == 0 else light_green

        pygame.draw.rect(self.screen, square_color,
                         self.__get_square_dimensions(coordinates))

        piece_at_square = self.board.get_piece(coordinates)

        if piece_at_square:
            self.__display_piece(piece_at_square)

    def __get_square_dimensions(self: Game, coordinates: Coordinates) -> tuple[int, int, int, int]:
        board_margin = board_border_thickness * 2 + board_edge_thickness

        left_margin = board_margin + square_size * coordinates.x
        top_margin = board_margin + square_size * coordinates.y

        return (left_margin, top_margin, square_size, square_size)

    def __display_piece(self: Game, piece: Piece) -> None:
        piece_icon = pygame.image.load('icons/%s_%s.png' % (piece.color.name, piece.type.name))
        left_margin, top_margin, square_size, square_size = self.__get_square_dimensions(piece.coordinates)

        scaled_piece_icon = pygame.transform.scale(piece_icon, (square_size, square_size))
        self.screen.blit(scaled_piece_icon, (left_margin, top_margin))
