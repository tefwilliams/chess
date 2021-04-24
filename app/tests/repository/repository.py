from chess import Piece, PieceTypes, Color, Coordinates, Bishop, King, Knight, Pawn, Queen, Rook

y_grid_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
x_grid_values = ['8', '7', '6', '5', '4', '3', '2', '1']


def generate_piece(piece_type: PieceTypes, coordinates_as_string: str, color: Color) -> Piece:
    coordinates = get_coordinates_from_grid_value(coordinates_as_string)

    if piece_type == PieceTypes.bishop:
        return Bishop(coordinates, color)

    if piece_type == PieceTypes.king:
        return King(coordinates, color)

    if piece_type == PieceTypes.knight:
        return Knight(coordinates, color)

    if piece_type == PieceTypes.pawn:
        return Pawn(coordinates, color)

    if piece_type == PieceTypes.queen:
        return Queen(coordinates, color)

    if piece_type == PieceTypes.rook:
        return Rook(coordinates, color)

    raise ValueError("Invalid piece type")


def get_coordinates_from_grid_value(coordinates: str) -> Coordinates:
    y_value = y_grid_values.index(coordinates[0])
    x_value = x_grid_values.index(coordinates[1])
    return Coordinates(y_value, x_value)
