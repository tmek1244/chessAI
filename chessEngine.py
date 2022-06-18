from common import translate, Coords, BoardField
from pieces.pieces import PieceType, PieceColor, create_piece


class Board:
    def __init__(self, empty=False):
        self.board = BoardField()
        self.history = []

        if not empty:
            self.reset()

    def reset(self):
        self.board.clear()

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

        if piece.type == PieceType.PAWN:
            pass
            # TODO en passant

        if piece.can_move(destination, self.board):
            if self._is_legal():
                self.board.move(start, destination)

        return 0

    def _is_legal(self):
        ...


if __name__ == '__main__':
    board = Board()
    print(board.make_move('e7', 'a2'))
