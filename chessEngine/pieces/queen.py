from chessEngine.common import (BoardField, Coords, Piece, PieceColor,
                                PieceType)
from typing import cast


class Queen(Piece):
    def __init__(self, color: PieceColor, position: Coords) -> None:
        super().__init__(PieceType.QUEEN, color, position)

    def _can_move(self, end, board: BoardField) -> bool:
        # row_start, col_start = translate(self.position)
        # row_dest, col_dest = translate(end)
        
        # move or take
        if (self.position.row == end.row or
                self.position.col == end.col or
                self.position.diagonal(end)):
            return not board.is_between(self.position, end) and self.king_not_under_check(end, board)
        return False
    
    def enemy_king_under_check(self, board: BoardField, position: Coords = None) -> bool:
        if position is None:
            position = self.position
        
        # row, col = translate(position)
        enemy_king = cast(Coords, board.kings[(self.color+1)%2].position)
        # king_row, king_col = translate(enemy_king.position)

        # if row != king_row and col != king_col and abs(row - king_row) != abs(col - king_col):
        #     return False
        # if row == king_row and not board.is_between(position, enemy_king.position):
        #     return True
        # if col == king_col and not board.is_between(position, enemy_king.position):
        #     return True
        # if abs(row - king_row) == abs(col - king_col) and not board.is_between(position, enemy_king.position):
        #     return True
        if (
            (
                position.diagonal(enemy_king) or 
                position.same_col(enemy_king) or 
                position.same_row(enemy_king)
            ) and not board.is_between(position, enemy_king)
        ):
            return True
        return False

    def get_all_moves(
        self, board: BoardField, whose_move: PieceColor|None = None) -> list[tuple[int, int]]:
        result = []
        if whose_move is not None and whose_move != self.color:
            return []

        for i, j in [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]:
            next_row, next_col = self.position.row + i, self.position.col + j
            while True:
                next_position = Coords((next_row, next_col))
                if not next_position.is_correct():
                    break
                can_move = self.can_move(next_position, board)[0]
                if not can_move and board.under_check[self.color] is None:
                    break
                if can_move:
                    result.append((next_row, next_col))
                next_row, next_col = next_row + i, next_col + j
        return result
