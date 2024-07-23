from .movement import Movement


class Move(Movement):
    def __init__(self, primary_movement: Movement, *other_movements: Movement) -> None:
        super().__init__(
            primary_movement.origin,
            primary_movement.destination,
            primary_movement.attack_location,
        )

        self.movements = tuple([primary_movement, *other_movements])
