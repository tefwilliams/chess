class Vector(tuple[int, int]):
    def __init__(self, col: int, row: int) -> None:
        self.__col = col
        self.__row = row

    @property
    def col(self):
        return self.__col

    @property
    def row(self):
        return self.__row

    def __new__(cls, col: int, row: int):
        return super().__new__(cls, (col, row))

    def __add__(self, other: "Vector | int") -> "Vector":
        if type(other) is int:
            return Vector(self.col + other, self.row + other)

        if type(other) is Vector:
            return Vector(self.col + other.col, self.row + other.row)

        raise ValueError("Addition must be either Vector or int")

    def __mul__(self, mutiple: int) -> "Vector":
        return Vector(self.col * mutiple, self.row * mutiple)
