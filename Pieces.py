from abc import ABC, abstractmethod
from enum import Enum


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


class Piece:
    def __init__(
            self,
            piece_type: PieceType,
            piece_color: PieceColor
    ):
        self.type = piece_type
        self.color = piece_color

    def __str__(self):
        match self.type:
            case PieceType.PAWN:
                return "P"
            case PieceType.ROOK:
                return "R"
            case PieceType.KNIGHT:
                return "N"
            case PieceType.BISHOP:
                return "B"
            case PieceType.QUEEN:
                return "Q"
            case PieceType.KING:
                return "K"

    def __repr__(self):
        return self.__str__()