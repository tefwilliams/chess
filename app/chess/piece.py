from enum import Enum
from .color import Color
from .vector import Vector


class PieceType(Enum):
    King = 0
    Queen = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Pawn = 5


class Piece:
    def __init__(self, type: PieceType, color: Color, coordinates: Vector):
        self.type = type
        self.color = color
        self.coordinates = coordinates
        self.coordinates_history: list[Vector] = []

    def move(self, new_coordinates: Vector):
        self.coordinates_history.append(self.coordinates)
        self.coordinates = new_coordinates

    def revert_last_move(self):
        old_coordinates = self.coordinates_history.pop()
        self.coordinates = old_coordinates

    @property
    def has_moved(self):
        return len(self.coordinates_history) > 0
