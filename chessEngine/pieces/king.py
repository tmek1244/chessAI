from chessEngine.common import translate, Coords, Piece, PieceType, PieceColor, BoardField


class King(Piece):
    def __init__(self, color, position):
        super().__init__(PieceType.KING, color, position)

    def _can_move(self, end: Coords, board: BoardField) -> bool | tuple[bool, str]:
        # if not super().can_move(end, board):
        #     return False
        row_start, col_start = translate(self.position)
        row_dest, col_dest = translate(end)

        # normal move
        if abs(row_start - row_dest) + abs(col_start - col_dest) == 1:
            return not self.under_check()

        # Board makes sure that both rook and king haven't moved yet
        # short castle
        if self._can_castle_short(row_dest, col_dest, board):
            return True, "short"
        if self._can_castle_long(row_dest, col_dest, board):
            return True, "long"

        return False

    def under_check(self, position: Coords = None):
        return False

    def _can_castle_short(self, row_dest, col_dest, board: BoardField):
        return (
            (not board.is_between(self.position, (row_dest, 7))) and
            (not self.when_moved) and
            (not self.under_check(self.position)) and
            (not self.under_check((row_dest, 5))) and
            (not self.under_check((row_dest, 6))) and
            (row_dest == 0 if self.color == PieceColor.WHITE else row_dest == 7) and
            (col_dest == 6) and
            (board[(row_dest, 7)].type == PieceType.ROOK) and
            (not board[(row_dest, 7)].when_moved)
        )

    def _can_castle_long(self, row_dest, col_dest, board: BoardField):
        return (
            (not self.when_moved) and
            (not board.is_between(self.position, (row_dest, 0))) and
            (not self.under_check(self.position)) and
            (not self.under_check((row_dest, 3))) and
            (not self.under_check((row_dest, 2))) and
            (row_dest == 0 if self.color == PieceColor.WHITE else row_dest == 7) and
            (col_dest == 2) and
            (board[(row_dest, 0)].type == PieceType.ROOK) and
            (not board[(row_dest, 0)].when_moved)
        )
