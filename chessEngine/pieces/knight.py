from chessEngine.common import translate, Coords, Piece, PieceType, PieceColor, BoardField



class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.KNIGHT, color, position)

    def _can_move(self, end, board: BoardField) -> bool:
        # if not super().can_move(end, board):
        #     return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        if ((abs(row_start - row_dest) == 2 and abs(col_start - col_dest) == 1)
                or (abs(row_start - row_dest) == 1
                    and abs(col_start - col_dest) == 2)):
            return True
        return False
