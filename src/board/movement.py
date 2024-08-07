from ..vector import Vector


class Movement:
    def __init__(
        self, origin: Vector, destination: Vector, attack_location: Vector | None = None
    ) -> None:
        self.origin = origin
        self.destination = destination
        self.attack_location = attack_location or destination
