from abc import ABC, abstractmethod
from enum import Enum

from chessEngine import BoardField
from common import translate


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
            piece_color: PieceColor,
            position: str
    ):
        self.type = piece_type
        self.color = piece_color
        self.position = position

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

    def can_move(
            self,
            end: str | tuple[int, int],
            board: BoardField
    ) -> bool | tuple[bool, str]:
        return not (board[end] and board[end].color == self.color)
