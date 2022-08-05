from chessEngine.common import translate, Coords, Piece, PieceType, PieceColor, BoardField


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.QUEEN, color, position)

    def _can_move(self, end, board: BoardField):
        # if not super().can_move(end, board):
        #     return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # move or take
        if (row_start == row_dest or
                col_start == col_dest or
                abs(row_start - row_dest) == abs(col_start - col_dest)):
            return not board.is_between(self.position, end)
        return False
