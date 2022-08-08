from chessEngine.common import translate, Coords, Piece, PieceType, PieceColor, BoardField

import logging
log = logging.getLogger(__name__)


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.PAWN, color, position)

    def _can_move(
            self, end: Coords, board: BoardField) -> bool | tuple[bool, str]:
        info = ""
        # if not super().can_move(end, board):
        #     return False, info
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # log.debug(f"{row_start}, {col_start}, {row_dest}, {col_dest}")
        if self._will_promote(row_dest):
            info = "promote"
        # move by one
        if self._move_by_one(row_start, col_start, row_dest, col_dest):
            return (board[end] is None and self.king_not_under_check(end, board)), info
        # move by two
        if self._move_by_two(row_start, col_start, row_dest, col_dest):
            return (not board.is_between(self.position, end)
                    and board[end] is None and self.king_not_under_check(end, board)), info

        # take
        if self._take(row_start, col_start, row_dest, col_dest):
            # normal take
            if board[end]:
                return self.king_not_under_check(end, board), info
            # en passant
            if self._en_passant(row_start, col_dest, board):
                return self.king_not_under_check(end, board), "en_passant"
            return False

        return False
    
    def _will_promote(self, row_dest):
        return (
            (self.color == PieceColor.WHITE and row_dest == 7) or
            (self.color == PieceColor.BLACK and row_dest == 0)
        )

    def _move_by_one(self, row_start, col_start, row_dest, col_dest):
        return (
            col_start == col_dest and
            (row_start + 1 == row_dest 
            if self.color == PieceColor.WHITE 
            else row_start - 1 == row_dest)
        )
    
    def _move_by_two(self, row_start, col_start, row_dest, col_dest):
        return (
            col_start == col_dest and
            (row_start == 1 if self.color == PieceColor.WHITE else row_start == 6) and
            (row_dest == 3 if self.color == PieceColor.WHITE else row_dest == 4)
        )
    
    def _take(self, row_start, col_start, row_dest, col_dest):
        return (
            (abs(col_dest - col_start) == 1) and
            (row_start + 1 == row_dest 
            if self.color == PieceColor.WHITE 
            else row_start - 1 == row_dest)
        )

    def _en_passant(self, row_start, col_dest, board: BoardField):
        return (
            (board[row_start, col_dest]) and
            (board[row_start, col_dest].type == PieceType.PAWN) and
            (board[row_start, col_dest].color != self.color) and
            (row_start == 4 if self.color == PieceColor.WHITE else row_start == 3) and 
            (board[row_start, col_dest].when_moved[-1] == board.move_counter) and
            (len(board[row_start, col_dest].when_moved) == 1)
        )

    def enemy_king_under_check(self, board: BoardField, position = None):
        if position is None:
            position = self.position
        
        row, col = translate(position)
        enemy_king = board.kings[(self.color+1)%2]
        king_row, king_col = translate(enemy_king.position)

        if (
            abs(col - king_col) == 1 and 
            (king_row + 1 == row if self.color == PieceColor.WHITE else king_row - 1 == row)):
            return True
        return False

    def get_all_moves(
        self, board: BoardField, whose_move: PieceColor|None = None) -> list[tuple[int, int]]:
        result = []
        if whose_move and whose_move != self.color:
            return []

        row, col = translate(self.position)
        for i, j in [(1, 0), (1, 1), (1, -1), (2, 0)]:
            if self.color == PieceColor.BLACK:
                i, j = i * -1, j * -1
            next_row, next_col = row + i, col + j
            if self.can_move((next_row, next_col), board)[0]:
                result.append((next_row, next_col))

        return result
