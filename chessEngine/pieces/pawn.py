import logging

from chessEngine.common import (BoardField, Coords, Piece, PieceColor,
                                PieceType)

log = logging.getLogger(__name__)


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.PAWN, color, position)

    def _can_move(
            self, end: Coords, board: BoardField) -> bool | tuple[bool, str]:
        info = ""
        # if not super().can_move(end, board):
        #     return False, info
        # row_start, col_start = translate(self.position)
        # row_dest, col_dest = translate(end)

        # log.debug(f"{row_start}, {col_start}, {row_dest}, {col_dest}")
        if self._will_promote(end.row):
            info = "promote"
        # move by one
        if self._move_by_one(self.position, end):
            return (board[end] is None and self.king_not_under_check(end, board)), info
        # move by two
        if self._move_by_two(self.position, end):
            return (not board.is_between(self.position, end)
                    and board[end] is None and self.king_not_under_check(end, board)), info

        # take
        if self._take(self.position, end):
            # normal take
            if board[end]:
                return self.king_not_under_check(end, board), info
            # en passant
            if self._en_passant(Coords((self.position.row, end.col)), board):
                return self.king_not_under_check(end, board), "en_passant"
            return False

        return False
    
    def _will_promote(self, row_dest: int) -> bool:
        return (
            (self.color == PieceColor.WHITE and row_dest == 7) or
            (self.color == PieceColor.BLACK and row_dest == 0)
        )

    def _move_by_one(self, start: Coords, end: Coords) -> bool:
        return (
            start.col == end.col and
            (start.row + 1 == end.row 
            if self.color == PieceColor.WHITE 
            else start.row - 1 == end.row)
        )
    
    def _move_by_two(self, start: Coords, end: Coords) -> bool:
        return (
            start.col == end.col and
            (start.row == 1 if self.color == PieceColor.WHITE else start.row == 6) and
            (end.row == 3 if self.color == PieceColor.WHITE else end.row == 4)
        )
    
    def _take(self, start: Coords, end: Coords) -> bool:
        return (
            (abs(end.col - start.col) == 1) and
            (start.row + 1 == end.row 
            if self.color == PieceColor.WHITE 
            else start.row - 1 == end.row)
        )

    def _en_passant(self, coords: Coords, board: BoardField) -> bool:
        return (
            ((enemy:=board[coords]) is not None) and
            (enemy.type == PieceType.PAWN) and
            (enemy.color != self.color) and
            (coords.row == 4 if self.color == PieceColor.WHITE else coords.row == 3) and 
            (enemy.when_moved[-1] == board.move_counter) and
            (len(enemy.when_moved) == 1)
        )

    def enemy_king_under_check(self, board: BoardField, position = None) -> bool:
        if position is None:
            position = self.position
        
        # row, col = translate(position)
        enemy_king = board.kings[(self.color+1)%2].position
        # king_row, king_col = translate(enemy_king.position)

        if (
            abs(position.col - enemy_king.col) == 1 and 
            (enemy_king.row + 1 == position.row if self.color == PieceColor.WHITE else enemy_king.row - 1 == position.row)):
            return True
        return False

    def get_all_moves(
        self, board: BoardField, whose_move: PieceColor|None = None) -> list[tuple[int, int]]:
        result = []
        if whose_move and whose_move != self.color:
            return []

        for i, j in [(1, 0), (1, 1), (1, -1), (2, 0)]:
            if self.color == PieceColor.BLACK:
                i, j = i * -1, j * -1
            next_row, next_col = self.position.row + i, self.position.col + j
            if self.can_move(Coords((next_row, next_col)), board)[0]:
                result.append((next_row, next_col))

        return result
