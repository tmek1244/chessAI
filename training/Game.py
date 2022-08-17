# https://github.com/suragnair/alpha-zero-general/blob/master/Game.py


import chess
import numpy as np


class Game():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        self.chess_board = chess.Board()

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (8, 8)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return 64*64

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        from_square = action//64
        to_square = action%64
        if player == chess.BLACK:
            from_square = 63 - from_square
            to_square = 63 - to_square
        self.chess_board.set_fen(board)
        
        move = chess.Move(from_square, to_square)
        self.chess_board.push(move) 
        return (self.chess_board.fen(), chess.Color(not player))

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        result = np.zeros(self.getActionSize())
        for move in self.chess_board.legal_moves:
            result[move.from_square*64 + move.to_square] = 1

        return result

        # return [move.uci() for move in ]

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        self.chess_board.set_fen(board)
        outcome = self.chess_board.outcome()

        if outcome is None:
            return 0
        if outcome.winner is None:
            return 0.05
        if outcome.winner == player:
            return 1
        return -1


    def getCanonicalForm(self, board: str, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        if player == chess.WHITE:
            return board
        
        board_splited = board.split()
        board_splited[0] = board_splited[0].swapcase()[::-1]
        board_splited[1] = 'w' if board_splited[1] == 'b' else 'b'
        board_splited[2] = board_splited[2].swapcase()

        castling = ""
        for letter in ['K', 'Q', 'k', 'q']:
            if letter in board_splited[2]:
                castling += letter
        if castling == "":
            castling = "-"
        board_splited[2] = castling

        if board_splited[3] != '-':
            row = '4' if board_splited[3][1] == '3' else '3'
            col = {
                'a': 'h',
                'b': 'g',
                'c': 'f',
                'd': 'e',
                'e': 'd',
                'f': 'c',
                'g': 'b',
                'h': 'a'
            }[board_splited[3][0]]
            board_splited[3] = col + row
        
        return ' '.join(board_splited)

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        return [(board, pi)]

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        
        return ' '.join(board.split()[:-2])
