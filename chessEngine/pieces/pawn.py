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
            return board[end] is None, info
        # move by two
        if self._move_by_two(row_start, col_start, row_dest, col_dest):
            return (not board.is_between(self.position, end)
                    and board[end] is None), info

        # take
        if self._take(row_start, col_start, row_dest, col_dest):
            # normal take
            if board[end]:
                return True, info
            # en passant
            if self._en_passant(row_start, col_dest, board):
                return True, "en_passant"
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
