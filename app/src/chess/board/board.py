
from __future__ import annotations
from ..repository import each
from ..coordinates import Coordinates
from ..movement import Movement
from ..player import Color
from ..pieces import Piece, PieceTypes
from ..data import board_size


class Board:
    size = board_size

    def __init__(self: Board, pieces: list[Piece]) -> None:
        self.__pieces = pieces

        self.__move_counter = 0
        self.__pieces_moved: list[tuple[int, Piece]] = []

        self.update_possible_moves()

    @property
    def pieces(self: Board) -> list[Piece]:
        return self.__pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = list(
            filter(lambda piece: piece.coordinates == coordinates, self.pieces))

        if len(pieces_with_coordinates) == 0:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" %
                               Coordinates.convert_to_grid_value(coordinates))

        return pieces_with_coordinates.pop()

    # TODO - rename this to move piece?
    def evaluate_move(self: Board, piece: Piece, coordinates: Coordinates) -> None:
        if coordinates not in piece.possible_moves:
            raise ValueError("You cannot make this move")

        is_en_passent = self.legal_en_passant(piece, coordinates)

        self.__move_piece(
            piece, coordinates, is_en_passent)

        self.__pieces_moved.append((self.__move_counter, piece))
        self.update_possible_moves()

    def increment_move_counter(self: Board) -> None:
        self.__move_counter += 1

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates, is_en_passent: bool) -> None:
        direction = piece.color.get_opposing_color().get_step_forward()
        coordinates_to_take_piece_from = coordinates.move_by(
            direction) if is_en_passent else coordinates

        piece_to_take = self.get_piece(coordinates_to_take_piece_from)

        if piece_to_take:
            self.__pieces.remove(piece_to_take)

        piece.move(coordinates)

    def __restore(self: Board, moved_piece: Piece, removed_piece: Piece | None) -> None:
        moved_piece.revert_last_move()

        if removed_piece and removed_piece not in self.__pieces:
            self.__pieces.append(removed_piece)

    def update_possible_moves(self: Board) -> None:
        each(lambda piece: piece.update_possible_moves(self), self.__pieces[:])

    def get_legal_moves(self: Board, piece: Piece, moves: list[list[Coordinates]]) -> list[Coordinates]:
        pseudo_legal_moves = self.get_unobstructed_squares(piece.color, moves)
        return list(filter(lambda coordinates: not self.__will_be_in_check_after_move(piece, coordinates), pseudo_legal_moves))

    def __will_be_in_check_after_move(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        piece_at_destination = self.get_piece(coordinates)
        # TODO - think about en passent
        self.__move_piece(piece, coordinates, False)

        in_check = self.is_in_check(piece.color)
        self.__restore(piece, piece_at_destination)

        return in_check

    def get_unobstructed_squares(self: Board, color: Color, squares: list[list[Coordinates]]) -> list[Coordinates]:
        unobstructed_squares: list[Coordinates] = []

        for squares_in_direction in squares:  # TODO - clarify what this is doing
            for square in squares_in_direction:
                piece_at_destination = self.get_piece(square)

                if piece_at_destination and piece_at_destination.color != color:
                    unobstructed_squares.append(square)
                    break

                elif piece_at_destination:
                    break

                unobstructed_squares.append(square)

        return unobstructed_squares

    def legal_en_passant(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        y = -1 if piece.color == Color.white else 1

        piece_at_destination = self.get_piece(coordinates.move_by((y, 0)))

        if not piece_at_destination:
            return False

        last_piece_to_move = self.__get_last_piece_to_move()

        piece_has_just_moved_two_squares = abs(
            piece_at_destination.coordinates.y - piece_at_destination.previous_coordinates.y) == 2

        return (piece.type == PieceTypes.pawn
                and piece_at_destination.color != piece.color
                and piece_at_destination.type == PieceTypes.pawn
                and piece_at_destination == last_piece_to_move
                and piece_has_just_moved_two_squares)

    def __get_last_piece_to_move(self: Board) -> Piece | None:
        if len(self.__pieces_moved) == 0:
            return None

        return self.__pieces_moved[-1][1]

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

        return any(map(lambda squares_and_pieces: self.__enemy_piece_is_at_square(*squares_and_pieces, enemy_color), squares_to_check_for_pieces))

    def __enemy_piece_is_at_square(self, list_of_squares: list[Coordinates], list_of_pieces: list[PieceTypes], enemy_color: Color) -> bool:
        return any(map(lambda piece: piece and piece.color ==
                       enemy_color and piece.type in list_of_pieces, map(self.get_piece, list_of_squares)))

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
        return any(len(piece.possible_moves) > 0 for piece in player_pieces)

    def check_mate(self: Board, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self: Board, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)
