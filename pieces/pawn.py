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
            # move by one
            if col_dest == col_start and row_start + 1 == row_dest:
                return board[end] is None
            # move by two
            if col_dest == col_start and row_start == 1 and row_dest == 3:
                return (not board.is_between(self.position, end)
                        and board[end] is None)
            # take
            if abs(col_dest - col_start) == 1 and row_start + 1 == row_dest:
                # normal take
                if board[end]:
                    return True
                # en passant
                if (row_start == 4 and
                        board[row_start, col_dest] and
                        board[row_start, col_dest].type == PieceType.PAWN):
                    return True
                return False

        if self.color == PieceColor.BLACK:
            # move by one
            if col_dest == col_start and row_start - 1 == row_dest:
                return board[end] is None
            # move by two
            if col_dest == col_start and row_start == 6 and row_dest == 4:
                return (not board.is_between(self.position, end)
                        and board[end] is None)

            # take
            if abs(col_dest - col_start) == 1 and row_start - 1 == row_dest:
                # normal take
                if board[end]:
                    return True
                # en passant
                if (row_start == 4 and
                        board[row_start, col_dest] and
                        board[row_start, col_dest].type == PieceType.PAWN):
                    return True
                return False
        return False
