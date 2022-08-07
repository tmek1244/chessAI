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

    def enemy_king_under_check(self, board: BoardField, position = None):
        if position is None:
            position = self.position
        
        row, col = translate(position)
        enemy_king = board.kings[(self.color+1)%2]
        king_row, king_col = translate(enemy_king.position)

        if row != king_row and col != king_col and abs(row - king_row) != abs(col - king_col):
            return False
        if abs(row - king_row) == abs(col - king_col) and not board.is_between(position, enemy_king.position):
            return True
        return False
