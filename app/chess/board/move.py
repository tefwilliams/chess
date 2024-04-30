from .movement import Movement


class Move(tuple[Movement]):
    def __init__(self, *movements: Movement) -> None:
        self.primary_movement = movements[0]
        self.additional_movements = movements[1:]

    def __new__(cls, *movements: Movement):
        return super().__new__(cls, movements)
