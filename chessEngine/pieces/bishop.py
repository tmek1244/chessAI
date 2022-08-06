from chessEngine.common import translate, Coords, Piece, PieceType, PieceColor, BoardField


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.BISHOP, color, position)

    def _can_move(self, end, board: BoardField) -> bool:
        # if not super().can_move(end, board):
        #     return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # move or take
        if abs(row_start - row_dest) == abs(col_start - col_dest):
            return not board.is_between(self.position, end) and self.king_not_under_check(end, board)
        return False
