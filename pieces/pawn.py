from chessEngine import BoardField
from common import translate
from pieces.pieces import Piece, PieceType, PieceColor


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.PAWN, color, position)

    def can_move(self, end, board: BoardField):
        if not super().can_move(end, board):
            return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        if self.color == PieceColor.WHITE:
            if not (row_start < row_dest < row_start + 2):
                return False
            if row_start + 2 == row_dest:
                if board.is_between(self.position, end):
                    return False
                return True
            if col_dest != col_start:
                if abs(col_dest - col_start) != 1:
                    return False
                if board[end]:
                    return True
                if (board[row_start, col_dest]
                        and board[row_start, col_dest].type == PieceType.PAWN):
                    return True, "en_passant"
                return False
            else:
                if board[end]:
                    return 7
                board.move(self.position, end)
                return 0

        if self.color == PieceColor.BLACK:
            if not (row_start > row_dest > row_start - 2):
                return False
            if row_start - 2 == row_dest:
                if board.is_between(self.position, end):
                    return False
                return True
            if col_dest != col_start:
                if abs(col_dest - col_start) != 1:
                    return False
                if board[end]:
                    return True
                if (board[row_start, col_dest]
                        and board[row_start, col_dest].type == PieceType.PAWN):
                    return True, "en_passant"
                return False
            else:
                if board[end]:
                    return 7
                board.move(self.position, end)
                return 0
