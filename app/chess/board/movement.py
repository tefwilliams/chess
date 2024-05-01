from ..piece import Piece
from ..vector import Vector


class Movement:
    def __init__(
        self, piece: Piece, destination: Vector, attack_location: Vector | None = None
    ) -> None:
        # TODO - change this to be start and finish coords
        self.piece = piece
        self.destination = destination
        self.attack_location = attack_location or destination