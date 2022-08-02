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
        if abs(row_start - row_dest) <= 1 and abs(col_start - col_dest) <= 1:
            return not self.under_check(board, (row_dest, col_dest))

        # Board makes sure that both rook and king haven't moved yet
        # short castle
        if self._can_castle_short(row_dest, col_dest, board):
            return True, "short"
        if self._can_castle_long(row_dest, col_dest, board):
            return True, "long"

        return False

    def _run_trace(self, cur_position, ver, hor, board):
        counter = 1
        
        for position in [(cur_position[0] + ver * i, cur_position[1] + hor * i) for i in range(1, 8)]:
            if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                return None
            if board[position]:
                return None if board[position].color == self.color else (board[position], counter)
            counter += 1
        return None
            

    def under_check(self, board, position: Coords = None):
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            piece_n_counter = self._run_trace(position, *direction, board)
            if piece_n_counter:
                piece, counter = piece_n_counter
                if piece.type == PieceType.QUEEN or piece.type == PieceType.ROOK:
                    return True
                if counter == 1 and piece.type == PieceType.KING:
                    return True
        
        for direction in [(1, 1), (1, -1)]:
            piece_n_counter = self._run_trace(position, *direction, board) 
            if piece_n_counter:
                piece, counter = piece_n_counter
                if piece.type == PieceType.QUEEN or piece.type == PieceType.BISHOP:
                    return True
                if counter == 1 and piece.type == PieceType.KING:
                    return True
                if self.color == PieceColor.WHITE and counter == 1 and piece.type == PieceType.PAWN:
                    return True
        
        for direction in [(-1, 1), (-1, -1)]:
            piece_n_counter = self._run_trace(position, *direction, board) 
            if piece_n_counter:
                piece, counter = piece_n_counter
                if piece.type == PieceType.QUEEN or piece.type == PieceType.BISHOP:
                    return True
                if counter == 1 and piece.type == PieceType.KING:
                    return True
                if self.color == PieceColor.BLACK and counter == 1 and piece.type == PieceType.PAWN:
                    return True

        return False

    def _can_castle_short(self, row_dest, col_dest, board: BoardField):
        return (
            (not board.is_between(self.position, (row_dest, 7))) and
            (not self.when_moved) and
            (not self.under_check(board, self.position)) and
            (not self.under_check(board, (row_dest, 5))) and
            (not self.under_check(board, (row_dest, 6))) and
            (row_dest == 0 if self.color == PieceColor.WHITE else row_dest == 7) and
            (col_dest == 6) and
            (board[(row_dest, 7)].type == PieceType.ROOK) and
            (not board[(row_dest, 7)].when_moved)
        )

    def _can_castle_long(self, row_dest, col_dest, board: BoardField):
        return (
            (not self.when_moved) and
            (not board.is_between(self.position, (row_dest, 0))) and
            (not self.under_check(board, self.position)) and
            (not self.under_check(board, (row_dest, 3))) and
            (not self.under_check(board, (row_dest, 2))) and
            (row_dest == 0 if self.color == PieceColor.WHITE else row_dest == 7) and
            (col_dest == 2) and
            (board[(row_dest, 0)].type == PieceType.ROOK) and
            (not board[(row_dest, 0)].when_moved)
        )
