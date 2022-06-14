from pprint import pprint
from typing import List, Union, Optional

from Pieces import Piece, PieceType, PieceColor


class Board:
    def __init__(self):
        self.board: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.reset()

    def reset(self):
        for i, piece in enumerate([
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]):
            self.board[0][i] = Piece(piece, PieceColor.WHITE)
            self.board[1][i] = Piece(PieceType.PAWN, PieceColor.WHITE)
            self.board[6][i] = Piece(PieceType.PAWN, PieceColor.BLACK)
            self.board[7][i] = Piece(piece, PieceColor.BLACK)

    def move(self, start, destination):
        pass


if __name__ == '__main__':
    board = Board()
    pprint(board.board)
