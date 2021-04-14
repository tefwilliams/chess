
from __future__ import annotations

from ..repository import each
from ..coordinates import Coordinates, Direction
from ..movement import Movement
from ..player import Color
from ..pieces import Piece, PieceTypes
from ..data import board_size


class Board:
    size = board_size

    def __init__(self: Board, pieces: list[Piece]) -> None:
        self.__pieces = pieces
        self.__last_piece_to_move = None
        self.update_possible_moves()

    @property
    def pieces(self: Board) -> list[Piece]:
        return self.__pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = [
            piece for piece in self.__pieces if piece.coordinates == coordinates]

        if len(pieces_with_coordinates) == 0:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" %
                               Coordinates.convert_to_grid_value(coordinates))

        return pieces_with_coordinates.pop()

    def evaluate_move(self: Board, piece_at_origin: Piece, destination_coordinates: Coordinates, should_move: bool = True) -> None:
        piece_at_destination = self.get_piece(destination_coordinates)

        if destination_coordinates not in piece_at_origin.possible_moves:
            raise ValueError("You cannot make this move")

        if not piece_at_destination and piece_at_origin.type == PieceTypes.pawn and self.en_passant_valid(destination_coordinates, piece_at_origin.color):
            y = -1 if piece_at_origin.color == Color.white else 1
            piece_at_destination = self.get_piece(
                Direction((y, 0)).step(destination_coordinates))

        self.__move_piece(
            piece_at_origin, destination_coordinates, piece_at_destination)

        if self.is_in_check(piece_at_origin.color):
            self.__restore(piece_at_origin, piece_at_destination)
            raise ValueError(
                "You can't make this move because it will leave you in check")

        elif not should_move:
            self.__restore(piece_at_origin, piece_at_destination)

        else:
            self.__last_piece_to_move = piece_at_origin
            self.update_possible_moves()

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates, piece_at_destination: Piece | None) -> None:
        if piece_at_destination:
            self.__pieces.remove(piece_at_destination)

        piece.move(coordinates)

    def __restore(self: Board, moved_piece: Piece, removed_piece: Piece | None) -> None:
        moved_piece.revert_last_move()

        if removed_piece and removed_piece not in self.__pieces:
            self.__pieces.append(removed_piece)

    def update_possible_moves(self: Board) -> None:
        each(lambda piece: piece.update_possible_moves(self), self.__pieces)

    def get_valid_moves(self: Board, piece: Piece, moves: list[list[Coordinates]]) -> list[Coordinates]:
        valid_moves = self.get_unobstructed_squares(piece.color, moves)
        return list(filter(lambda coordinates: not self.__move_puts_king_in_check(piece, coordinates), valid_moves))

    def __move_puts_king_in_check(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        piece_at_destination = self.get_piece(coordinates)
        self.__move_piece(piece, coordinates, piece_at_destination)

        in_check = self.is_in_check(piece.color)
        self.__restore(piece, piece_at_destination)

        return in_check

    def get_unobstructed_squares(self: Board, color: Color, squares: list[list[Coordinates]]) -> list[Coordinates]:
        unobstructed_squares: list[Coordinates] = []

        for list_of_squares in squares:  # TODO - clarify what this is doing
            for square in list_of_squares:
                piece_at_destination = self.get_piece(square)

                if piece_at_destination and piece_at_destination.color != color:
                    unobstructed_squares.append(square)
                    break

                elif piece_at_destination:
                    break

                unobstructed_squares.append(square)

        return unobstructed_squares

    def en_passant_valid(self: Board, coordinates: Coordinates, color: Color) -> bool:
        y = -1 if color == Color.white else 1

        direction = Direction((y, 0))
        piece_at_destination = self.get_piece(direction.step((coordinates)))

        if not piece_at_destination:
            return False

        piece_has_just_moved_two_squares = abs(
            piece_at_destination.coordinates.y - piece_at_destination.previous_coordinates.y) == 2

        return (piece_at_destination.color != color
                and piece_at_destination.type == PieceTypes.pawn
                and piece_at_destination == self.__last_piece_to_move
                and piece_has_just_moved_two_squares)

    # TODO - pull methods onto player?
    def is_in_check(self: Board, color: Color) -> bool:
        king = self.__get_king(color)
        return king is not None and self.square_is_attacked(king.coordinates, color)

    def square_is_attacked(self: Board, coordinates: Coordinates, color: Color) -> bool:
        diagonal_squares = self.get_unobstructed_squares(
            color, Movement.get_diagonal_squares(coordinates))
        orthogonal_squares = self.get_unobstructed_squares(
            color, Movement.get_orthogonal_squares(coordinates))
        knight_squares = self.get_unobstructed_squares(
            color, Movement.get_knight_squares(coordinates))
        adjacent_squares = self.get_unobstructed_squares(
            color, Movement.get_adjacent_squares(coordinates))
        pawn_attack_squares = self.get_unobstructed_squares(
            color, Movement.get_pawn_attack_squares(coordinates, color))

        enemy_color = Color.get_opposing_color(color)

        squares_to_check_for_pieces = [
            (diagonal_squares, [PieceTypes.bishop, PieceTypes.queen]),
            (orthogonal_squares, [PieceTypes.rook, PieceTypes.queen]),
            (pawn_attack_squares, [PieceTypes.pawn]),
            (knight_squares, [PieceTypes.knight]),
            (adjacent_squares, [PieceTypes.king])
        ]

        return any(self.__enemy_piece_is_at_square(list_of_squares, list_of_pieces, enemy_color) for list_of_squares, list_of_pieces in squares_to_check_for_pieces)

    def __enemy_piece_is_at_square(self, list_of_squares: list[Coordinates], list_of_pieces: list[PieceTypes], enemy_color: Color) -> bool:
        for square in list_of_squares:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color == enemy_color and piece_at_destination.type in list_of_pieces:
                return True

        return False

    def __can_any_piece_move(self: Board, pieces: list[Piece], coordinates: Coordinates) -> bool:
        for piece in pieces:
            try:
                self.evaluate_move(piece, coordinates, False)

            except ValueError:
                pass

            else:
                return True

        return False

    def __get_king(self: Board, color: Color) -> Piece | None:
        player_pieces = self.__get_pieces_by_color(color)
        player_king_list = list(
            filter(lambda piece: piece.type == PieceTypes.king, player_pieces))

        if len(player_king_list) > 1:
            raise RuntimeError("More than one king on %s team" % color.name)

        if len(player_king_list) == 0:
            return None

        return player_king_list.pop()

    def __get_pieces_by_color(self: Board, color: Color) -> list[Piece]:
        return list(filter(lambda piece: piece.color == color, self.pieces))

    def __any_possible_moves(self: Board, color: Color) -> bool:
        player_pieces = self.__get_pieces_by_color(color)
        list_of_coordinates = [Coordinates((y, x)) for y in range(
            self.size) for x in range(self.size)]

        # TODO - change this to piece first to make more readable
        # also should end up being that length of possible moves is zero
        return any(self.__can_any_piece_move(player_pieces, coordinates) for coordinates in list_of_coordinates)

    def check_mate(self: Board, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self: Board, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)
