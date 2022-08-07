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
            return self.king_not_under_check(end, board)
        return False
    
    def enemy_king_under_check(self, board: BoardField, position = None):
        if position is None:
            position = self.position
        
        row, col = translate(position)
        enemy_king = board.kings[(self.color+1)%2]
        king_row, king_col = translate(enemy_king.position)

        if abs(row - king_row) + abs(col - king_col) == 3 and 0 < abs(row - king_row) < 3:
            return True 
        return False
