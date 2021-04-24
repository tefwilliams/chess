
from __future__ import annotations
from typing import Callable
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
        self.__pieces_moved: dict[int, Piece] = {}
        self.__pieces_taken: dict[int, Piece] = {}

        self.__update_possible_moves()

    @property
    def pieces(self: Board) -> list[Piece]:
        return self.__pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = [
            piece for piece in self.__pieces if piece.coordinates == coordinates]

        if not pieces_with_coordinates:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" % coordinates)

        return pieces_with_coordinates.pop()

    # TODO - rename this to move piece?
    def evaluate_move(self: Board, piece: Piece, coordinates: Coordinates) -> None:
        if coordinates not in piece.possible_moves:
            raise ValueError("You cannot make this move")

        self.__move_piece(piece, coordinates)
        self.__update_possible_moves()
        self.__move_counter += 1

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates) -> Callable[[], None]:
        moved_pieces = self.__pieces_moved.copy()
        taken_pieces = self.__pieces_taken.copy()
        current_pieces = self.__pieces[:]

        piece_to_take = self.__get_piece_to_take(piece, coordinates)

        if piece_to_take:
            self.__pieces.remove(piece_to_take)
            self.__pieces_taken[self.__move_counter] = piece_to_take

        piece.move(coordinates)
        self.__pieces_moved[self.__move_counter] = piece

        def undo_move() -> None:
            piece.revert_last_move()
            self.__pieces = current_pieces
            self.__pieces_moved = moved_pieces
            self.__pieces_taken = taken_pieces

        return undo_move

    def __get_piece_to_take(self: Board, piece: Piece, coordinates: Coordinates) -> Piece | None:
        is_en_passant = self.legal_en_passant(piece, coordinates)
        step_backward = piece.color.get_opposing_color().get_step_forward()

        coordinates_to_take_piece_from = coordinates.move_by(
            step_backward) if is_en_passant else coordinates

        return self.get_piece(coordinates_to_take_piece_from)

    def __update_possible_moves(self: Board) -> None:
        for piece in self.__pieces[:]:
            piece.update_possible_moves(self)

    def get_legal_moves(self: Board, piece: Piece, all_moves: list[list[Coordinates]]) -> list[Coordinates]:
        pseudo_legal_moves = self.__get_unobstructed_squares(
            piece.color, all_moves)
        return [coordinates for coordinates in pseudo_legal_moves if not self.__will_be_in_check_after_move(piece, coordinates)]

    def __will_be_in_check_after_move(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        undo_move = self.__move_piece(piece, coordinates)
        in_check = self.is_in_check(piece.color)
        undo_move()

        return in_check

    def __get_unobstructed_squares(self: Board, color: Color, squares: list[list[Coordinates]]) -> list[Coordinates]:
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
        step_backward = piece.color.get_opposing_color().get_step_forward()
        piece_to_take = self.get_piece(coordinates.move_by(step_backward))

        if not piece_to_take:
            return False

        last_piece_to_move = self.__get_last_piece_to_move()

        piece_has_just_moved_two_squares = abs(
            piece_to_take.coordinates.y - piece_to_take.previous_coordinates.y) == 2

        return (piece.type == PieceTypes.pawn
                and piece_to_take.color != piece.color
                and piece_to_take.type == PieceTypes.pawn
                and piece_to_take == last_piece_to_move
                and piece_has_just_moved_two_squares)

    # TODO - implement logic
    def legal_castle(self: Board) -> bool:
        raise NotImplementedError

    def __get_last_piece_to_move(self: Board) -> Piece | None:
        if not self.__pieces_moved:
            return None

        return list(self.__pieces_moved.values()).pop()

    # TODO - pull methods onto player?
    def is_in_check(self: Board, color: Color) -> bool:
        king = self.__get_king(color)
        return king is not None and self.square_is_attacked(king.coordinates, color)

    def square_is_attacked(self: Board, coordinates: Coordinates, color: Color) -> bool:
        diagonal_squares = self.__get_unobstructed_squares(
            color, Movement.get_diagonal_squares(coordinates))
        orthogonal_squares = self.__get_unobstructed_squares(
            color, Movement.get_orthogonal_squares(coordinates))
        knight_squares = self.__get_unobstructed_squares(
            color, Movement.get_knight_squares(coordinates))
        adjacent_squares = self.__get_unobstructed_squares(
            color, Movement.get_adjacent_squares(coordinates))
        pawn_attack_squares = self.__get_unobstructed_squares(
            color, Movement.get_pawn_attack_squares(coordinates, color))

        enemy_color = Color.get_opposing_color(color)

        squares_to_check_for_pieces = [
            (diagonal_squares, [PieceTypes.bishop, PieceTypes.queen]),
            (orthogonal_squares, [PieceTypes.rook, PieceTypes.queen]),
            (pawn_attack_squares, [PieceTypes.pawn]),
            (knight_squares, [PieceTypes.knight]),
            (adjacent_squares, [PieceTypes.king])
        ]

        return any(self.__enemy_piece_is_at_square(*squares_and_pieces, enemy_color) for squares_and_pieces in squares_to_check_for_pieces)

    def __enemy_piece_is_at_square(self, list_of_squares: list[Coordinates], list_of_pieces: list[PieceTypes], enemy_color: Color) -> bool:
        return any(piece and piece.color == enemy_color and piece.type in list_of_pieces for piece in map(self.get_piece, list_of_squares))

    # TODO - does this need to ever return None?
    # can we mock the reponse if there is no king?
    def __get_king(self: Board, color: Color) -> Piece | None:
        player_pieces = self.__get_pieces_by_color(color)
        player_king_list = [
            piece for piece in player_pieces if piece.type == PieceTypes.king]

        if len(player_king_list) > 1:
            raise RuntimeError("More than one king on %s team" % color.name)

        if not player_king_list:
            return None

        return player_king_list.pop()

    def __get_pieces_by_color(self: Board, color: Color) -> list[Piece]:
        return [piece for piece in self.__pieces if piece.color == color]

    def __any_possible_moves(self: Board, color: Color) -> bool:
        player_pieces = self.__get_pieces_by_color(color)
        return any(piece.possible_moves for piece in player_pieces)

    def check_mate(self: Board, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self: Board, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)
