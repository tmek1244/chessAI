from abc import ABC, abstractmethod


class PieceType:
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Piece(ABC):
    def __init__(self, start_position: tuple, piece_type: PieceType):
        self.position = start_position
        self.type = piece_type

    @abstractmethod
    def can_move(self):
        pass
