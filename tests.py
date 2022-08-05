from copy import deepcopy
from chessEngine.chessEngine import Board
from chessEngine.common import PieceColor


def possible_moves_step(engine_board, color, counter):
    board = engine_board.board
    if counter < 1:
        return 1
    next_color = PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE
    sum = 0
    for piece in board.pieces:
        for move in piece.get_all_moves(board, color):
            engine = deepcopy(engine_board)
            if engine.make_move(piece.position, move) == 0:
                sum += possible_moves_step(engine, next_color, counter-1)
    return sum
    

def test_possible_moves():
    engine_board = Board()

    # moves = 0
    # for piece in engine_board.board.pieces:
    #     moves += len(piece.get_all_moves(engine_board.board, PieceColor.WHITE))
    
    print(possible_moves_step(engine_board, PieceColor.WHITE, 5))
        

def main():
    test_possible_moves()


if __name__ == '__main__':
    main()
