from chessEngine.common import translate, Coords, BoardField, PieceType, PieceColor
from chessEngine.pieces.pieces import create_piece

import logging

log = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)

class Board:
    def __init__(self, empty=False):
        log.info("Creating board...")
        self.board = BoardField()
        self.history = []
        self.next_move = PieceColor.WHITE

        if not empty:
            self.reset()

    def reset(self):
        self.board.clear()
        self.next_move: PieceColor = PieceColor.WHITE

        for i, piece in enumerate([
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]):
            self.board[0, i] = create_piece(
                piece, PieceColor.WHITE, (0, i))
            self.board[1, i] = create_piece(
                PieceType.PAWN, PieceColor.WHITE, (1, i))
            self.board[6, i] = create_piece(
                PieceType.PAWN, PieceColor.BLACK, (6, i))
            self.board[7, i] = create_piece(
                piece, PieceColor.BLACK, (7, i))

        self.history = []

    def make_move(
            self,
            start: Coords,
            destination: Coords,
            next_piece: PieceType = None):
        piece = self.board[start]
        if not piece:
            return 1

        row_start, col_start = translate(start)
        row_dest, col_dest = translate(destination)

        if piece.color != self.next_move:
            log.error(f"It's now a {self.next_move} move")
            return 0

        if piece.type == PieceType.PAWN:
            pass
            # TODO en passant
        can_move, info = piece.can_move(destination, self.board)
        log.info(info)
        if not can_move:
            return 0

        if info == 'short':
            ...

        if self._is_legal():
            self.board.move(start, destination)
            self.next_move = (
                PieceColor.BLACK if self.next_move == PieceColor.WHITE 
                else PieceColor.WHITE
            )

        return 0

    def _is_legal(self):
        return True


if __name__ == '__main__':
    board = Board()
    print(board.make_move('e7', 'a2'))
