from copy import deepcopy
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
        self.move_counter = 0

        if not empty:
            self.reset()

    def reset(self):
        self.board.clear()
        self.next_move: PieceColor = PieceColor.WHITE
        self.move_counter = 0

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
            return 1

        can_move, info = piece.can_move(destination, self.board)
        log.info(info)
        if not can_move:
            return 1

        board_copy = deepcopy(self.board)
        if info == 'short':
            board_copy.move(start, destination, self.move_counter)
            board_copy.move((row_start, 7), (row_start, 5), self.move_counter)
        elif info == "long":
            board_copy.move(start, destination, self.move_counter)
            board_copy.move((row_start, 0), (row_start, 3), self.move_counter)
        elif info == "en_passant":
            board_copy.en_passant(start, destination, self.move_counter)
        else:
            board_copy.move(start, destination, self.move_counter)
        if self._is_legal(board_copy):
            if info == 'short':
                self.board.move(start, destination, self.move_counter)
                self.board.move((row_start, 7), (row_start, 5), self.move_counter)
            elif info == "long":
                self.board.move(start, destination, self.move_counter)
                self.board.move((row_start, 0), (row_start, 3), self.move_counter)
            elif info == "en_passant":
                self.board.en_passant(start, destination, self.move_counter)
            else:
                self.board.move(start, destination, self.move_counter)
        else:
            return 1

        self.next_move = (
                PieceColor.BLACK if self.next_move == PieceColor.WHITE 
                else PieceColor.WHITE
            )
        self.move_counter += 1
        return 0

    def _is_legal(self, board: BoardField):
        for piece in board.pieces:
            if piece.type == PieceType.KING and piece.color == self.next_move and piece.under_check(board, piece.position):
                return False
        return True


if __name__ == '__main__':
    board = Board()
    print(board.make_move('e7', 'a2'))
