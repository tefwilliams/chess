
from __future__ import annotations
from movement import Movement
from player import Player
from pieces.pieces import Pieces
from pieces.piece import Piece
from coordinates import Coordinates


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

    def evaluate_move(self: Board, player: Player, piece: Piece, coordinates: Coordinates) -> None:
        if piece.coordinates == coordinates:
            raise ValueError("Can't move piece to same location")

        if self.__move_obstructed(piece.coordinates, coordinates):
            raise ValueError("Movement obstucted by another piece")

        piece_at_destination = self.get_piece(coordinates)

        if not piece_at_destination:
            piece.move(coordinates, self)

        elif piece_at_destination.color != player:
            piece.move(coordinates, self)
            self.__pieces.remove(piece_at_destination)

        else:
            raise ValueError("You cannot move to a space occupied by one of your pieces")

        if self.__in_check():
            raise ValueError("You can't make this move because it will leave you in check")

    def __move_obstructed(self: Board, starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        movement_steps = Movement.get_steps(starting_coordinates, finishing_coordinates)
        movement_steps.pop(0) # Remove starting coordinates

        for step in movement_steps:
            if self.get_piece(step):
                return True

        return False

    def __in_check(self: Board) -> bool:
        return False
