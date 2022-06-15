from typing import Optional

from pieces import Piece, PieceType, PieceColor
from common import translate


class BoardField:
    def __init__(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def __getitem__(self, item) -> Optional[Piece]:
        row, col = translate(item)
        return self.board[row][col]

    def __setitem__(self, key, value) -> None:
        row, col = translate(key)
        self.board[row][col] = value

    def is_between(self, start, end):
        row_start, col_start = translate(start)
        row_end, col_end = translate(end)

        if row_start == row_end:
            min_col, max_col = min(col_start, col_end), max(col_start, col_end)
            for i in range(min_col + 1, max_col):
                if self.board[row_start][i]:
                    return True
            return False
        if col_start == col_end and row_start > row_end:
            min_row, max_row = min(row_start, row_end), max(row_start, row_end)
            for i in range(min_row + 1, max_row):
                if self.board[row_start][i]:
                    return True
            return False
        if abs(row_start - row_end) == abs(col_start - col_end):
            min_row = min(row_start, row_end)
            if row_end == min_row:
                row_start, row_end = row_end, row_start
                col_start, col_end = col_end, col_start

            for i in range(1, abs(row_start - row_end)):
                if (col_start < col_end
                        and self.board[row_start + i][col_start + i]):
                    return True
                elif (col_start > col_end
                      and self.board[row_start + i][col_start - i]):
                    return True

    def move(self, start, end):
        row_start, col_start = translate(start)
        row_end, col_end = translate(end)

        self.board[row_end][col_end] = self.board[row_start][col_start]
        self.board[row_start][col_start] = None


class Board:
    def __init__(self):
        self.board = BoardField()
        self.history = []
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
            self.board[0, i] = Piece(piece, PieceColor.WHITE)
            self.board[1, i] = Piece(PieceType.PAWN, PieceColor.WHITE)
            self.board[6, i] = Piece(PieceType.PAWN, PieceColor.BLACK)
            self.board[7, i] = Piece(piece, PieceColor.BLACK)

        self.history = []

    def _move(self, start, destination):
        piece = self.board[start]
        if not piece:
            return 1

        row_start, col_start = translate(start)
        row_dest, col_dest = translate(destination)

        if piece.type == PieceType.PAWN:
            pass
            # TODO en passant
        if piece.can_move(destination, self.board):
            self.board.move(start, destination)

        return 0

    def _is_legal(self):
        pass


if __name__ == '__main__':
    board = Board()
    print(board._move('e7', 'a2'))
