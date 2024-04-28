from ..vector import Vector
from ..shared import only, last
from ..errors import InvalidMove
from ..color import Color
from ..piece import Piece, PieceType
from ..movement import Move, get_adjacent_squares, get_unit_step_backward


class Board:
    def __init__(self, pieces: set[Piece]) -> None:
        self.pieces = pieces
        self.__moved_pieces: list[Piece] = []

    def try_get_piece(self, coordinates: Vector) -> Piece | None:
        return next(
            (piece for piece in self.pieces if piece.coordinates == coordinates), None
        )

    def get_piece(self, coordinates: Vector) -> Piece:
        piece = self.try_get_piece(coordinates)

        if piece is None:
            raise ValueError(f"No piece found for coordinates: {coordinates}")

        return piece

    def move(self, move: Move) -> None:
        if move.destination not in self.get_possible_moves(move.piece):
            raise InvalidMove(
                f"You cannot move {move.piece.type.name} to {move.destination}"
            )

        self.__move_piece(move)

    def __move_piece(self, move: Move):
        if move.destination in self.get_legal_castle_moves(move.piece.coordinates):
            castle_squares = [
                square
                for squares_in_direction in get_castle_squares(move.piece)
                for square in squares_in_direction
                if move.destination in squares_in_direction
            ]
            castle_to_move = self.try_get_piece(castle_squares[-1])
            assert castle_to_move
            castle_to_move.move(castle_squares[0])

        # TODO - handle en passant
        piece_to_take = self.try_get_piece(move.destination)

        if piece_to_take:
            self.pieces.remove(piece_to_take)

        move.piece.move(move.destination)
        self.__moved_pieces.append(move.piece)

    # TODO - something like destinations (to avoid confusion with Move)
    def get_possible_moves(self, piece: Piece) -> list[Vector]:
        return [
            pseudo_legal_move
            for pseudo_legal_move in self.__get_pseudo_legal_moves(piece)
            if not self.__will_be_in_check_after_move(Move(piece, pseudo_legal_move))
        ] + self.get_legal_castle_moves(piece.coordinates)

    def __will_be_in_check_after_move(self, move: Move) -> bool:
        move.piece.move(move.destination)
        is_in_check = self.is_in_check(move.piece.color)
        move.piece.revert_last_move()

        return is_in_check

    def __get_pseudo_legal_moves(self, piece: Piece) -> list[Vector]:
        return [
            move
            # TODO - get moves for piece
            for moves_in_direction in get_adjacent_squares(piece.coordinates)
            for move in self.__get_unobstructed_moves_in_direction(
                piece.color, moves_in_direction
            )
        ]

    def __get_unobstructed_moves_in_direction(
        self, color: Color, moves_in_direction: list[Vector]
    ) -> list[Vector]:
        unobstructed_moves_in_direction: list[Vector] = []

        for square in moves_in_direction:
            piece_at_destination = self.try_get_piece(square)

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
    def legal_en_passant(self, move: Move) -> bool:
        if move.piece.type != PieceType.Pawn:
            return False

        step_backward = get_unit_step_backward(move.piece.color)
        piece_to_take = self.try_get_piece(move.piece.coordinates + step_backward)

        if (
            not piece_to_take
            or piece_to_take.color == move.piece.color
            or piece_to_take.type != PieceType.Pawn
        ):
            return False

        piece_has_just_moved_two_squares = (
            previous_coords := last(piece_to_take.coordinates_history)
        ) is not None and abs(piece_to_take.coordinates.row - previous_coords.row) == 2

        return (
            piece_to_take == self.last_piece_to_move
            and piece_has_just_moved_two_squares
        )

    def get_legal_castle_moves(self, coordinates: Vector) -> list[Vector]:
        piece = self.try_get_piece(coordinates)
        return []

        if piece is None or piece.type != PieceType.King or piece.has_moved:
            return []

        return [
            squares_in_direction[1]
            for squares_in_direction in get_castle_squares(piece.coordinates)
            if self.__legal_castle(piece, squares_in_direction[1])
        ]

    def __legal_castle(self, piece: Piece, coordinates: Vector) -> bool:
        castle_squares = [
            square
            for squares_in_direction in Movement.get_castle_squares(piece.coordinates)
            for square in squares_in_direction
            if coordinates in squares_in_direction
        ]

        return (
            piece.type == PieceType.King
            and len(castle_squares) > 0
            and (possible_rook := self.try_get_piece(castle_squares[-1])) is not None
            and possible_rook.type == PieceType.Rook
            and not piece.has_moved
            and not possible_rook.has_moved
            and coordinates == castle_squares[1]
            and not self.is_in_check(piece.color)
            and not any(
                self.__square_is_attacked(square, piece.color)
                for square in castle_squares[0:1]
            )
            and all(
                self.try_get_piece(square) is None for square in castle_squares[0:-1]
            )
        )

    # TODO - Maybe init Move with start as well
    def get_last_move(self) -> tuple[Vector, Vector] | None:
        return (
            (previous_coordinates, last_piece_to_move.coordinates)
            if (last_piece_to_move := self.last_piece_to_move)
            and (previous_coordinates := last(last_piece_to_move.coordinates_history))
            else None
        )

    def is_in_check(self, color: Color) -> bool:
        return (
            king := self.__get_king(color)
        ) is not None and self.__square_is_attacked(king.coordinates, color)

    def __square_is_attacked(self, coordinates: Vector, color: Color) -> bool:
        return any(
            # Square attacked by piece
            any(
                piece_at_square
                and piece_at_square.color != piece.color
                and piece_at_square.type == piece.type
                for piece_at_square in (
                    self.try_get_piece(square)
                    for square in self.__get_pseudo_legal_moves(piece)
                )
            )
            for piece in (
                Piece(type, color, coordinates)
                for type in [
                    PieceType.Pawn,
                    PieceType.Rook,
                    PieceType.Knight,
                    PieceType.Bishop,
                    PieceType.Queen,
                    PieceType.King,
                ]
            )
        )

    def __get_king(self, color: Color) -> Piece | None:
        return only(
            (
                piece
                for piece in self.__get_pieces_by_color(color)
                if piece.type == PieceType.King
            ),
            f"More than one king on {color.name} team",
        )

    def __get_pieces_by_color(self, color: Color) -> list[Piece]:
        return [piece for piece in self.pieces if piece.color == color]

    def __any_possible_moves(self, color: Color) -> bool:
        return any(
            any(self.get_possible_moves(piece))
            for piece in self.__get_pieces_by_color(color)
        )

    def check_mate(self, color: Color) -> bool:
        return self.is_in_check(color) and not self.__any_possible_moves(color)

    def stale_mate(self, color: Color) -> bool:
        return not self.is_in_check(color) and not self.__any_possible_moves(color)

    @property
    def last_piece_to_move(self):
        return last(self.__moved_pieces)
