
from __future__ import annotations
from ...src.coordinates import Coordinates, Direction
from ...src.movement import Movement
from ...src.player import Color
from ...src.pieces import Piece, PieceTypes


class Board:
    size = Coordinates.maximum_size

    def __init__(self: Board, pieces: list[Piece]) -> None:
        self.__pieces = pieces
        self.update_all_possible_moves()

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = [piece for piece in self.__pieces if piece.coordinates == coordinates]

        if len(pieces_with_coordinates) == 0:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" % Coordinates.convert_to_grid_value(coordinates))

        return pieces_with_coordinates.pop()

    def evaluate_move(self: Board, piece: Piece, coordinates: Coordinates, should_move: bool = True) -> None:
        piece_at_destination = self.get_piece(coordinates)

        if coordinates not in piece.possible_moves:
            raise ValueError("You cannot make this move")

        self.__move_piece(piece, coordinates, piece_at_destination) 

        if self.is_in_check(piece.color):
            self.__restore(piece, piece_at_destination)
            raise ValueError("You can't make this move because it will leave you in check")

        elif not should_move:
            self.__restore(piece, piece_at_destination)

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates, piece_at_destination: Piece | None) -> None:
        if piece_at_destination:
            self.__pieces.remove(piece_at_destination)

        piece.move(coordinates)

    def __restore(self: Board, moved_piece: Piece, removed_piece: Piece | None) -> None:
        moved_piece.restore()

        if removed_piece and removed_piece not in self.__pieces:
            self.__pieces.append(removed_piece)

    def update_all_possible_moves(self: Board) -> None:
        for piece in self.__pieces:
            piece.update_possible_moves(self)

    def get_unobstructed_squares(self: Board, color: Color, squares: list[list[Coordinates]]) -> list[Coordinates]:
        unobstructed_squares: list[Coordinates] = []

        for list_of_squares in squares:
            for square in list_of_squares:
                piece_at_destination = self.get_piece(square)

                if piece_at_destination and piece_at_destination.color != color:
                    unobstructed_squares.append(square)
                    break

                elif piece_at_destination:
                    break

                unobstructed_squares.append(square)

        return unobstructed_squares

    # TODO - pull methods onto player?
    # TODO - need to take into account pawn movement logic
    def is_in_check(self: Board, color: Color) -> bool:
        king_coordinates = self.__get_king(color).coordinates

        diagonal_squares = self.get_unobstructed_squares(color, Movement.get_diagonal_squares(king_coordinates))
        orthogonal_squares = self.get_unobstructed_squares(color, Movement.get_orthogonal_squares(king_coordinates))
        knight_squares = self.get_unobstructed_squares(color, Movement.get_knight_squares(king_coordinates))
        adjacent_squares = self.get_unobstructed_squares(color, Movement.get_adjacent_squares(king_coordinates))

        vertical_direction = 1 if color == Color.white else -1

        for horizontal_direction in [-1, 1]:
            direction = Direction((vertical_direction, horizontal_direction))
            piece_at_destination = self.get_piece(direction.step(king_coordinates))

            if piece_at_destination and piece_at_destination.color != color and piece_at_destination.type == PieceTypes.pawn:
                return True

        for square in diagonal_squares:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color != color and (piece_at_destination.type == PieceTypes.bishop or piece_at_destination.type == PieceTypes.queen):
                return True

        for square in orthogonal_squares:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color != color and (piece_at_destination.type == PieceTypes.rook or piece_at_destination.type == PieceTypes.queen):
                return True

        for square in knight_squares:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color != color and piece_at_destination.type == PieceTypes.knight:
                return True

        for square in adjacent_squares:
            piece_at_destination = self.get_piece(square)

            if piece_at_destination and piece_at_destination.color != color and piece_at_destination.type == PieceTypes.king:
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

    def __get_king(self: Board, color: Color) -> Piece:
        king_with_color_list = [piece for piece in self.__pieces if piece.type == PieceTypes.king and piece.color == color]

        if len(king_with_color_list) > 1:
            raise ValueError("More than one king on %s team" % color.name)

        if len(king_with_color_list) == 0:
            raise ValueError("No king on %s team" % color.name)

        return king_with_color_list.pop()

    def __get_pieces_by_color(self: Board, color: Color) -> list[Piece]:
        return [piece for piece in self.__pieces if piece.color == color]

    def __any_possible_moves(self: Board, player: Color) -> bool:
        player_pieces = self.__get_pieces_by_color(player)

        for i in range(self.size):
            for j in range(self.size):
                coordinates = Coordinates((i, j))

                if self.__can_any_piece_move(player_pieces, coordinates):
                    return True

        return False

    def check_mate(self: Board, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self: Board, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)
