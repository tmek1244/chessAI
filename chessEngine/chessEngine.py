import logging
from copy import deepcopy
import numpy as np

from chessEngine.common import (BoardField, Coords, PieceColor, PieceType,
                                )
from chessEngine.pieces.pieces import create_piece
from .AI import Bot

log = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

bot = Bot()


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
                piece, PieceColor.WHITE, Coords((0, i)))
            self.board[1, i] = create_piece(
                PieceType.PAWN, PieceColor.WHITE, Coords((1, i)))
            self.board[6, i] = create_piece(
                PieceType.PAWN, PieceColor.BLACK, Coords((6, i)))
            self.board[7, i] = create_piece(
                piece, PieceColor.BLACK, Coords((7, i)))

        self.history = []

    def make_move(
            self,
            start: Coords,
            destination: Coords,
            next_piece: PieceType = None):
        if not isinstance(start, Coords):
            start = Coords(start)
        if not isinstance(destination, Coords):
            destination = Coords(destination)
        piece = self.board[start]
        if not piece:
            return 1

        if piece.color != self.next_move:
            # log.error(f"It's now a {self.next_move} move")
            return 1

        can_move, info = piece.can_move(destination, self.board)
        if info:
            log.info(f"Returned info: {info}")

        if not can_move:
            return 1

        if info == 'short':
            self.board.move(start, destination, self.move_counter)
            self.board.move(Coords((start.row, 7)), Coords((start.row, 5)), self.move_counter)
        elif info == "long":
            self.board.move(start, destination, self.move_counter)
            self.board.move(Coords((start.row, 0)), Coords((start.row, 3)), self.move_counter)
        elif info == "en_passant":  
            self.board.en_passant(start, destination, self.move_counter)
        elif info == "promote":
            if next_piece is None:
                return 2
            if next_piece in [PieceType.KING, PieceType.PAWN]:
                return 1
            new_piece = create_piece(next_piece, self.next_move, destination)
            self.board.promote(start, destination, new_piece)
            
        else:
            self.board.move(start, destination, self.move_counter)
        # else:
        #     return 1

        self.next_move = (
                PieceColor.BLACK if self.next_move == PieceColor.WHITE 
                else PieceColor.WHITE
            )
        self.move_counter += 1
    
        # if self.next_move == PieceColor.BLACK:
        #     self.bot_move()
        
        return 0
    
    def try_move(
            self,
            start: Coords,
            destination: Coords,
            next_piece: PieceType = None):
        if not isinstance(start, Coords):
            start = Coords(start)
        if not isinstance(destination, Coords):
            destination = Coords(destination)
        piece = self.board[start]
        if not piece:
            return 1

        if piece.color != self.next_move:
            # log.error(f"It's now a {self.next_move} move")
            return 1

        can_move, info = piece.can_move(destination, self.board)
        if not can_move:
            return 1
        return 0

    def bot_move(self):
        evalutaion = bot.evaluate(self.board.to_array())
        for i, idx in enumerate(np.argsort(evalutaion)[::-1]):
            from_square = idx//64
            to_square = idx%64
            if self.try_move(Coords((from_square//8, from_square%8)), Coords((to_square//8, to_square%8))) == 0:
                print(f"Best move {from_square} -> {to_square}, after {i} tries. Confidence: {evalutaion[idx]}")
                return self.make_move(Coords((from_square//8, from_square%8)), Coords((to_square//8, to_square%8)))
                    
        # best_move = ((None, None), 100)
        # for piece in self.board.pieces:
        #     for move in piece.get_all_moves(self.board, PieceColor.BLACK):
        #         # COUNTER += 1
        #         engine = deepcopy(self)
        #         if engine.make_move(piece.position, move) == 0:
        #             if (evalutaion:=bot.evaluate(engine.board.to_array())) < best_move[1]:
        #                 best_move = ((piece.position, move), evalutaion)
        #             print(f"move {piece.position} -> {move} with eval {evalutaion}")

        # print(f"Best move {best_move[0][0]} -> {best_move[0][1]} with eval {best_move[1]}")
        # self.make_move(*best_move[0])

    # def _is_legal(self, board: BoardField):
    #     for piece in board.pieces:
    #         if piece.type == PieceType.KING and piece.color == self.next_move and piece.under_check(board, piece.position):
    #             return False
    #     return True


if __name__ == '__main__':
    board = Board()
    print(board.make_move(Coords('e7'), Coords('a2')))
