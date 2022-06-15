from chessEngine import BoardField
from common import translate
from pieces.pieces import Piece, PieceType, PieceColor


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.KNIGHT, color, position)

    def can_move(self, end, board: BoardField):
        if not super().can_move(end, board):
            return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        if self.color == PieceColor.WHITE:
            pass
