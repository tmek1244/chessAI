from chessEngine.common import (BoardField, Coords, Piece, PieceColor,
                                PieceType)


class Knight(Piece):
    def __init__(self, color: PieceColor, position: Coords) -> None:
        super().__init__(PieceType.KNIGHT, color, position)

    def _can_move(self, end, board: BoardField) -> bool:
        # if not super().can_move(end, board):
        #     return False
        # row_start, col_start = translate(self.position)
        # row_dest, col_dest = translate(end)

        if abs(self.position.row - end.row) * abs(self.position.col - end.col) == 2:
            return self.king_not_under_check(end, board)
        return False
    
    def enemy_king_under_check(self, board: BoardField, position = None) -> bool:
        if position is None:
            position = self.position
        
        enemy_king = board.kings[(self.color+1)%2].position

        if abs(self.position.row - enemy_king.row) * abs(self.position.col - enemy_king.col) == 2:
            return True 
        return False

    def get_all_moves(
        self, board: BoardField, whose_move: PieceColor|None = None) -> list[tuple[int, int]]:
        result = []
        if whose_move is not None and whose_move != self.color:
            return []

        for i in [1, 2, -1, -2]:
            for j in [3 - abs(i), -3 + abs(i)]:
                next_row, next_col = self.position.row + i, self.position.col + j
                if self.can_move(Coords((next_row, next_col)), board)[0]:
                    result.append((next_row, next_col))

        return result
