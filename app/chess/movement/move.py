from ..piece import Piece
from ..vector import Vector


class Move:
    def __init__(self, piece: Piece, destination: Vector) -> None:
        self.piece = piece
        self.destination = destination
