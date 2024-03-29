from enum import Enum

import chessEngine.common as common
from chessEngine.pieces.bishop import Bishop
from chessEngine.pieces.king import King
from chessEngine.pieces.knight import Knight
# from chessEngine.common import BoardField, Coords
from chessEngine.pieces.pawn import Pawn
from chessEngine.pieces.queen import Queen
from chessEngine.pieces.rook import Rook
from ..common import Coords


def create_piece(
        piece: common.PieceType,
        color: common.PieceColor,
        position: str | tuple[int, int]) -> common.Piece:
    return {
        common.PieceType.PAWN: Pawn,
        common.PieceType.KNIGHT: Knight,
        common.PieceType.BISHOP: Bishop,
        common.PieceType.ROOK: Rook,
        common.PieceType.QUEEN: Queen,
        common.PieceType.KING: King
    }[piece](color, Coords(position))
