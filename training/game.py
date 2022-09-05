from cmath import sqrt
import chess

from collections import defaultdict


class Position:
    def __init__(self, fen=chess.STARTING_FEN, win=None) -> None:
        if win:
            if win.winner == True:
                self.result = 1
            elif win.winner == False:
                self.result = -1
            else:
                self.result = 0
        else:
            self.result = None
        self.fen = fen
    
    def __eq__(self, __o: object) -> bool:
        return self.fen == __o.fen    


class Game:
    def __init__(self) -> None:
        self.chess_board = chess.Board()

    def game_ended(self, position: Position):
        return position.result is not None

    def get_valid_actions(self, position: Position):
        self.chess_board.set_fen(position.fen)

        return [move.uci() for move in self.chess_board.legal_moves]
    
    def next_state(self, position: Position, move_uci: str):
        self.chess_board.set_fen(position.fen)

        move = chess.Move.from_uci(move_uci)
        self.chess_board.push(move) 
        return Position(self.chess_board.fen(), self.chess_board.outcome())


    
    # def get_curr_position(self) -> np.ndarray:
    #     result = np.zeros((2, 6, 8, 8))
    #     weak_stockfish.set_position(self.all_moves)
    #     for row in range(1, 9):
    #         for i, col in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
    #             piece = weak_stockfish.get_what_is_on_square(col+str(row))
    #             if not piece:
    #                 continue
                
    #             color = 1 if 'a' < piece.value < 'z' else 0
    #             piece_id = None
    #             if piece.value.lower() == 'k':
    #                 piece_id = 0
    #             elif piece.value.lower() == 'q':
    #                 piece_id = 1
    #             elif piece.value.lower() == 'r':
    #                 piece_id = 2
    #             elif piece.value.lower() == 'b':
    #                 piece_id = 3
    #             elif piece.value.lower() == 'n':
    #                 piece_id = 4
    #             elif piece.value.lower() == 'p':
    #                 piece_id = 5
    #             result[color, piece_id, row-1, i] = 1
    #     return result 

class MCTS:
    def __init__(self) -> None:
        self.Q = {}
        self.N = defaultdict(defaultdict)
        self.P = {}
        c_puct = 5
        self.visited = set()

    def search(self, s: Position, game: Game, nnet):
        if game.game_ended(s): return -s.result

        if s not in self.visited:
            self.visited.add(s)
            self.P[s], v = nnet.predict(s)
            return -v
    
        max_u, best_a = -float("inf"), -1
        for a in game.get_valid_actions(s):
            u = (
                self.Q[(s, a)] + 
                self.c_puct*self.P[(s, a)] * sqrt(sum(self.N[s].values()))/(1+self.N[s][a])
            )
            if u>max_u:
                max_u = u
                best_a = a
        a = best_a
        
        sp = game.next_state(s, a)
        v = self.search(sp, game, nnet)

        self.Q[(s, a)] = (self.N[s][a]*self.Q[(s, a)] + v)/(self.N[s][a]+1)
        self.N[s][a] += 1
        return -v


if __name__ == "__main__":
    position = Position()

    game = Game()
    print(game.get_valid_actions(position))

