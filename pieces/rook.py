from chessEngine import BoardField
from common import translate
from pieces.pieces import Piece, PieceType, PieceColor


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.ROOK, color, position)

    def _can_move(self, end, board: BoardField) -> bool:
        if not super().can_move(end, board):
            return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # move or take
        if row_start == row_dest or col_start == col_dest:
            return not board.is_between(self.position, end)
        return False
