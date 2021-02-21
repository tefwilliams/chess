
from __future__ import annotations
from movement import Movement
from player import Player
from pieces.pieces import Pieces
from pieces.piece import Piece, PieceTypes
from coordinates import Coordinates
from copy import deepcopy


class Board:
    shape = Coordinates((8, 8))

    def __init__(self: Board) -> None:
        self.initialize_pieces()

    def initialize_pieces(self: Board) -> None:
        board_dimensions = Board.shape
        pieces: list[Piece] = []

        for i in range(board_dimensions.y):
            for j in range(board_dimensions.x):
                coordinates = Coordinates((i, j))
                starting_piece = Pieces.get_starting_piece(coordinates)
                
                if starting_piece:
                    pieces.append(starting_piece)

        self.__pieces = pieces

    def get_piece(self: Board, coordinates: Coordinates) -> Piece | None:
        pieces_with_coordinates = [piece for piece in self.__pieces if piece.coordinates == coordinates]

        if len(pieces_with_coordinates) == 0:
            return None

        if len(pieces_with_coordinates) > 1:
            raise RuntimeError("More than one piece is at %s" % Coordinates.convert_to_grid_value(coordinates))

        return pieces_with_coordinates.pop()

    def evaluate_move(self: Board, piece: Piece, coordinates: Coordinates, should_move: bool = True) -> None:
        starting_coordinates = piece.coordinates
        piece_at_destination = self.get_piece(coordinates)

        if piece.coordinates == coordinates:
            raise ValueError("Can't move piece to same square")

        if not piece.can_move(coordinates, piece_at_destination):
            raise ValueError("A %s cannot move to that sqaure" % piece.type.name)

        if self.__move_obstructed(piece.coordinates, coordinates):
            raise ValueError("Movement obstucted by another piece")

        if piece_at_destination and piece_at_destination.player == piece.player:
            raise ValueError("You cannot move to a square occupied by one of your pieces")

        if should_move:
            self.__move_piece(piece, coordinates, piece_at_destination)

        if self.__in_check(piece.player):
            self.__restore(piece, starting_coordinates, piece_at_destination)
            raise ValueError("You can't make this move because it will leave you in check")

    def __move_piece(self: Board, piece: Piece, coordinates: Coordinates, piece_at_destination: Piece | None) -> None:
        if piece_at_destination:
            self.__pieces.remove(piece_at_destination)

        piece.move(coordinates)

    def __restore(self: Board, moved_piece: Piece, original_coordinates: Coordinates, removed_piece: Piece | None) -> None:
        moved_piece.move(original_coordinates)

        if removed_piece and removed_piece not in self.__pieces:
            self.__pieces.append(removed_piece)

    def __move_obstructed(self: Board, starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        movement_steps = Movement.get_steps(starting_coordinates, finishing_coordinates)
        movement_steps.pop(0) # Remove starting coordinates

        for step in movement_steps:
            if self.get_piece(step):
                return True

        return False

    # TODO - pull methods onto player?
    def __in_check(self: Board, player: Player) -> bool:
        king_coordinates = self.__get_king(player).coordinates

        opposing_player = Player.black if player == Player.white else Player.white
        opposing_player_pieces = self.get_player_pieces(opposing_player)

        return self.__can_any_piece_move(opposing_player_pieces, king_coordinates)

    def __can_any_piece_move(self: Board, pieces: list[Piece], coordinates: Coordinates) -> bool:
        for piece in pieces:
            try:
                self.evaluate_move(piece, coordinates, False)

            except ValueError:
                pass

            else:
                return True

        return False

    def __get_king(self: Board, player: Player) -> Piece:
        player_king_list = [piece for piece in self.__pieces if piece.type == PieceTypes.king and piece.player == player]

        if len(player_king_list) > 1:
            raise ValueError("More than one king on %s team" % player)

        if len(player_king_list) == 0:
            raise ValueError("No king on %s team" % player)

        return player_king_list.pop()

    def get_player_pieces(self: Board, player: Player) -> list[Piece]:
        return [piece for piece in self.__pieces if piece.player == player]

    def __any_possible_moves(self: Board, player: Player) -> bool:
        player_pieces = self.get_player_pieces(player)

        for i in range(self.shape.y):
            for j in range(self.shape.x):
                coordinates = Coordinates((i, j))

                if self.__can_any_piece_move(player_pieces, coordinates):
                    return True

        return False

    def check_mate(self: Board, player: Player) -> bool:
        can_get_out_of_check = self.__any_possible_moves(player)
        return self.__in_check(player) and not can_get_out_of_check

    def stale_mate(self: Board, player: Player) -> bool:
        can_move = self.__any_possible_moves(player)
        return not self.__in_check(player) and not can_move
