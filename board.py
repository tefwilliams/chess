
from __future__ import annotations
from movement import Movement
from player import Player
from pieces.pieces import Pieces
from pieces.piece import Piece, PieceTypes
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

        piece_at_destination = self.get_piece(coordinates)

        # Look at way to move this into piece moving perhaps?
        if not piece_at_destination:
            piece.move(coordinates, self)

        elif piece_at_destination.player != player:
            piece.move(coordinates, self)
            self.__pieces.remove(piece_at_destination)

        else:
            raise ValueError("You cannot move to a space occupied by one of your pieces")

        if self.__in_check(player):
            raise ValueError("You can't make this move because it will leave you in check")

    def move_obstructed(self: Board, starting_coordinates: Coordinates, finishing_coordinates: Coordinates) -> bool:
        movement_steps = Movement.get_steps(starting_coordinates, finishing_coordinates)
        movement_steps.pop(0) # Remove starting coordinates

        for step in movement_steps:
            if self.get_piece(step):
                return True

        return False

    # Pull methods onto player?
    def __in_check(self: Board, player: Player) -> bool:
        king = self.__get_king(player)

        opposing_team_pieces = [piece for piece in self.__pieces if piece.player != player]

        for piece in opposing_team_pieces:
            try:
                piece.move(king.coordinates, self)
                return True

            except:
                ValueError

        return False

    def __get_king(self: Board, player: Player) -> Piece:
        player_king_list = [piece for piece in self.__pieces if piece.type == PieceTypes.king and piece.player == player]

        if len(player_king_list) > 1:
            raise ValueError("More than one king on %s team" % player)

        if len(player_king_list) == 0:
            raise ValueError("No king on %s team" % player)

        return player_king_list.pop()

    def check_mate(self: Board, player: Player) -> bool:
        king = self.__get_king(player)
        possible_king_movements: list[Coordinates] = []

        for i in range(-1, 1):
            for j in range(-1, 1):
                if i == j == 0:
                    continue

                possible_king_movements.append(Coordinates((i, j)))

        king_can_move = False

        for movement in possible_king_movements:
            try:
                self.evaluate_move(player, king, movement)
                king_can_move = True

            except:
                ValueError

        return self.__in_check(player) and not king_can_move
