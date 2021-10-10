
from __future__ import annotations
from .helpers import only, flatten
from .grid import Coordinates
from .movement import Movement
from .color import Color
from .pieces import Piece, PieceTypes, Pawn, Rook, Knight, Bishop, Queen, King
from .data import board_size
from copy import deepcopy


class Board:
    size = board_size

    def __init__(self: Board, pieces: list[Piece]) -> None:
        self.__pieces = pieces

        self.__move_counter = 0
        self.__pieces_moved: dict[int, Piece] = {}
        self.__pieces_taken: dict[int, Piece] = {}

    @property
    def pieces(self: Board) -> list[Piece]:
        return self.__pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        return only((piece for piece in self.__pieces if piece.coordinates == coordinates), f"More than one piece is at {coordinates}")

    # TODO - rename this to move piece?
    def evaluate_move(self: Board, piece: Piece, coordinates: Coordinates) -> None:
        if coordinates not in self.get_legal_moves(piece):
            raise ValueError("You cannot make this move")

        self.__move_piece(piece, coordinates)
        self.__move_counter += 1

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates) -> None:
        piece_to_take = self.__get_piece_to_take(piece, coordinates)

        if piece_to_take:
            self.__pieces.remove(piece_to_take)
            self.__pieces_taken[self.__move_counter] = piece_to_take

        if coordinates in self.get_legal_castle_moves(piece):
            castle_squares = [
                square for squares_in_direction in Movement.get_castle_squares(piece.coordinates) for square in squares_in_direction if coordinates in squares_in_direction]
            castle_to_move = self.get_piece(castle_squares[-1])
            assert castle_to_move
            castle_to_move.move(castle_squares[0])

        piece.move(coordinates)
        self.__pieces_moved[self.__move_counter] = piece

    def __get_piece_to_take(self: Board, piece: Piece, coordinates: Coordinates) -> Piece | None:
        is_en_passant = self.legal_en_passant(piece, coordinates)
        step_backward = piece.color.get_opposing_color().get_step_forward()

        coordinates_to_take_piece_from = coordinates.move_by(
            step_backward) if is_en_passant else coordinates

        return self.get_piece(coordinates_to_take_piece_from)

    def get_legal_moves(self: Board, piece: Piece) -> list[Coordinates]:
        return [pseudo_legal_move for pseudo_legal_move in self.__get_pseudo_legal_moves(piece) if not self.__will_be_in_check_after_move(piece, pseudo_legal_move)] + self.get_legal_castle_moves(piece)

    def __will_be_in_check_after_move(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        current_board = deepcopy(self)
        current_piece = current_board.get_piece(piece.coordinates)

        assert current_piece

        current_board.__move_piece(current_piece, coordinates)
        return current_board.is_in_check(piece.color)

    def __get_pseudo_legal_moves(self: Board, piece: Piece) -> list[Coordinates]:
        return flatten([self.__get_unobstructed_moves_in_direction(piece.color, moves_in_direction) for moves_in_direction in piece.get_base_moves(self)])

    def __get_unobstructed_moves_in_direction(self: Board, color: Color, moves_in_direction: list[Coordinates]) -> list[Coordinates]:
        unobstructed_moves_in_direction: list[Coordinates] = []

        for square in moves_in_direction:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color != color:
                # Can move to square since enemy piece is there - can't move further
                unobstructed_moves_in_direction.append(square)
                break

            elif piece_at_destination:
                # Can't move to square because friendly piece is there
                break

            unobstructed_moves_in_direction.append(square)

        return unobstructed_moves_in_direction

    # TODO - change to get_legal_en_passant_moves
    def legal_en_passant(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        if piece.type != PieceTypes.pawn:
            return False

        step_backward = piece.color.get_opposing_color().get_step_forward()
        piece_to_take = self.get_piece(coordinates.move_by(step_backward))

        if (not piece_to_take
                or piece_to_take.color == piece.color
                or piece_to_take.type != PieceTypes.pawn):
            return False

        last_piece_to_move = self.__get_last_piece_to_move()

        piece_has_just_moved_two_squares = (piece_to_take.previous_coordinates is not None
                                            and abs(piece_to_take.coordinates.y - piece_to_take.previous_coordinates.y) == 2)

        return (piece_to_take == last_piece_to_move
                and piece_has_just_moved_two_squares)

    def get_legal_castle_moves(self: Board, piece: Piece) -> list[Coordinates]:
        if piece.type != PieceTypes.king or piece.has_moved:
            return []

        return [squares_in_direction[1] for squares_in_direction in Movement.get_castle_squares(
            piece.coordinates) if self.__legal_castle(piece, squares_in_direction[1])]

    def __legal_castle(self: Board, piece: Piece, coordinates: Coordinates) -> bool:
        castle_squares = [
            square for squares_in_direction in Movement.get_castle_squares(piece.coordinates) for square in squares_in_direction if coordinates in squares_in_direction]

        if len(castle_squares) == 0:
            return False

        piece_at_castle_position = self.get_piece(castle_squares[-1])

        return (piece.type == PieceTypes.king
                and piece_at_castle_position is not None
                and piece_at_castle_position.type == PieceTypes.rook
                and not piece.has_moved
                and not piece_at_castle_position.has_moved
                and coordinates == castle_squares[1]
                and not self.is_in_check(piece.color)
                and not any(self.__square_is_attacked(square, piece.color) for square in castle_squares[0: 1])
                and all(self.get_piece(square) is None for square in castle_squares[0: -1]))

    def __get_last_piece_to_move(self: Board) -> Piece | None:
        return list(self.__pieces_moved.values()).pop() if self.__pieces_moved else None

    def get_last_move(self: Board) -> tuple[Coordinates, Coordinates] | None:
        last_piece_to_move = self.__get_last_piece_to_move()

        return (last_piece_to_move.previous_coordinates, last_piece_to_move.coordinates) if last_piece_to_move and last_piece_to_move.previous_coordinates else None

    def is_in_check(self: Board, color: Color) -> bool:
        king = self.__get_king(color)
        return king is not None and self.__square_is_attacked(king.coordinates, color)

    def __square_is_attacked(self: Board, coordinates: Coordinates, color: Color) -> bool:
        pieces: list[Piece] = [piece(coordinates, color) for piece in [
            Pawn, Rook, Knight, Bishop, Queen, King]]

        return any(self.__sqaure_is_attacked_by_piece(piece) for piece in pieces)

    def __sqaure_is_attacked_by_piece(self: Board, piece: Piece) -> bool:
        return any(piece_at_square and piece_at_square.color != piece.color and piece_at_square.type == piece.type for piece_at_square in map(self.get_piece, self.__get_pseudo_legal_moves(piece)))

    def __get_king(self: Board, color: Color) -> Piece | None:
        player_pieces = self.__get_pieces_by_color(color)
        return only((piece for piece in player_pieces if piece.type == PieceTypes.king), f"More than one king on {color.name} team")

    def __get_pieces_by_color(self: Board, color: Color) -> list[Piece]:
        return [piece for piece in self.__pieces if piece.color == color]

    def __any_possible_moves(self: Board, color: Color) -> bool:
        player_pieces = self.__get_pieces_by_color(color)
        return any(self.get_legal_moves(piece) for piece in player_pieces)

    def check_mate(self: Board, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self: Board, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)
