from chessEngine import BoardField
from common import translate, Coords
from pieces.pieces import Piece, PieceType, PieceColor


class King(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.KING, color, position)
        self.moved = False

    def _can_move(self, end: Coords, board: BoardField) -> bool:
        if not super().can_move(end, board):
            return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # normal move
        if abs(row_start - row_dest) + abs(col_start - col_dest) == 1:
            return not self.under_check()

        # Board makes sure that both rook and king haven't moved yet
        # short castle
        if col_dest == 6 and self._can_castle_short():
            return True
        if col_dest == 2 and self._can_castle_long():
            return True

        return False

    def under_check(self, position: Coords = None):
        ...

    def _can_castle_short(self):
        ...

    def _can_castle_long(self):
        ...
