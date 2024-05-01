from .piece import Piece, PieceType
from ..vector import Vector


class BoardPiece(Piece):
    def move(self, new_coordinates: Vector):
        self._coordinates_history.append(self.coordinates)
        self._coordinates = new_coordinates

    @Piece.type.setter
    def type(self, new_type: PieceType):
        self._type = new_type
