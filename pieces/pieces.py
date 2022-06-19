from enum import Enum

from common import BoardField, Coords
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.queen import Queen
from pieces.king import King


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
            position: str | tuple[int, int]
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
    ) -> tuple[bool, str]:
        if board[end] and board[end].color == self.color:
            return False, "Cannot take own piece"

        output = self._can_move(end, board)
        return (output, "") if type(output) == bool else output

    def _can_move(
            self,
            end: Coords,
            board: BoardField
    ) -> bool | tuple[bool, str]:
        ...


def create_piece(
        piece: PieceType,
        color: PieceColor,
        position: str | tuple[int, int]) -> Piece:
    return {
        PieceType.PAWN: Pawn,
        PieceType.KNIGHT: Knight,
        PieceType.BISHOP: Bishop,
        PieceType.ROOK: Rook,
        PieceType.QUEEN: Queen,
        PieceType.KING: King
    }[piece](color, position)
