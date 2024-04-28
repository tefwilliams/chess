from ..piece import Piece
from ..vector import Vector


class BoardSquare(Vector):
    def __init__(self, coordinates: Vector, piece: Piece | None):
        super().__init__(*coordinates)

        self.piece = piece

    def __new__(cls, coordinates: Vector, _):
        return super().__new__(cls, *coordinates)
