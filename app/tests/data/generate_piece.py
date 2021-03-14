from app.src import Piece, PieceTypes, Color, Coordinates, Bishop, King, Knight, Pawn, Queen, Rook

def generate_piece(piece_type: PieceTypes, coordinates_as_string: str, color: Color) -> Piece:
    coordinates = Coordinates.convert_from_grid_value(coordinates_as_string)

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
