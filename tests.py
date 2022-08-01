from chessEngine.chessEngine import Board
from chessEngine.common import PieceColor


def test_possible_moves():
    engine_board = Board()

    moves = 0
    for piece in engine_board.board.pieces:
        moves += len(piece.get_all_moves(engine_board.board, PieceColor.WHITE))
    
    print(moves)
        

def main():
    test_possible_moves()


if __name__ == '__main__':
    main()
