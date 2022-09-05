from chessEngine.common import (BoardField, Coords, Piece, PieceColor,
                                PieceType)


class King(Piece):
    def __init__(self, color: PieceColor, position: Coords) -> None:
        super().__init__(PieceType.KING, color, position)

    def _can_move(self, end: Coords, board: BoardField) -> bool | tuple[bool, str]:
        # if not super().can_move(end, board):
        #     return False
        # row_start, col_start = translate(self.position)
        # end.row, col_dest = translate(end)

        # normal move
        if abs(self.position.row - end.row) <= 1 and abs(self.position.col - end.col) <= 1:
            return not self.under_check(board, end)

        # Board makes sure that both rook and king haven't moved yet
        # short castle
        if self._can_castle_short(end, board):
            return True, "short"
        if self._can_castle_long(end, board):
            return True, "long"

        return False

    def _run_trace(self, cur_position: Coords, ver, hor, board) -> tuple[Piece, int] | None:
        counter = 1
        
        for position in [(cur_position.row + ver * i, cur_position.col + hor * i) for i in range(1, 8)]:
            if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                return None
            if board[position] and board[position] != self:
                return None if board[position].color == self.color else (board[position], counter)
            counter += 1
        return None
            

    def under_check(self, board, _position: Coords | None = None) -> bool:
        position = self.position if _position is None else _position

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
        
        for i in [-2, 2]:
            for j in [1, -1]:
                piece1 = board[(position.row+i, position.col + j)]
                piece2 = board[(position.row+j, position.col + i)]
                if piece1 and piece1.color != self.color and piece1.type == PieceType.KNIGHT:
                    return True
                if piece2 and piece2.color != self.color and piece2.type == PieceType.KNIGHT:
                    return True

        return False

    def _can_castle_short(self, end: Coords, board: BoardField) -> bool:
        return (
            (not board.is_between(self.position, end)) and
            (not self.when_moved) and
            (not self.under_check(board)) and
            (not self.under_check(board, Coords((end.row, 5)))) and
            (not self.under_check(board, Coords((end.row, 6)))) and
            (end.row == 0 if self.color == PieceColor.WHITE else end.row == 7) and
            (end.col == 6) and
            ((rook:=board[(end.row, 7)]) is not None) and
            (rook.type == PieceType.ROOK) and
            (not rook.when_moved)
        )

    def _can_castle_long(self, end: Coords, board: BoardField) -> bool:
        return (
            (not self.when_moved) and
            (not board.is_between(self.position, Coords((end.row, 0)))) and
            (not self.under_check(board)) and
            (not self.under_check(board, Coords((end.row, 3)))) and
            (not self.under_check(board, Coords((end.row, 2)))) and
            (end.row == 0 if self.color == PieceColor.WHITE else end.row == 7) and
            (end.col == 2) and
            ((rook:=board[(end.row, 0)]) is not None) and
            (rook.type == PieceType.ROOK) and
            (not rook.when_moved)
        )

    def enemy_king_under_check(self, board: BoardField, position = None) -> bool:
        return False

    def get_all_moves(
        self, board: BoardField, whose_move: PieceColor|None = None) -> list[tuple[int, int]]:
        result = []
        if whose_move is not None and whose_move != self.color:
            return []

        for i, j in [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
            (0, 2), (0, -2)
            ]:
            next_row, next_col = self.position.row + i, self.position.col + j
            if self.can_move(Coords((next_row, next_col)), board)[0]:
                result.append((next_row, next_col))
        return result
