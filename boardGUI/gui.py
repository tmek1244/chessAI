import pygame

import logging

# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level = logging.DEBUG)
log = logging.getLogger(__name__)


from piece import PieceGUI
from chessEngine.chessEngine import Board

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class BoardGui:
    def __init__(self, screen, engine_board, pieces_gui) -> None:
        self.screen = screen
        self.running = True
        self.engine_board: Board = engine_board
        self.pieces_gui: PieceGUI = pieces_gui
        self.piece_pressed = None
        self.possible_moves = []

    def run(self):
        while self.running:
            self.loop()

    def set_board(self):
        white_field = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//8))
        self.screen.fill((118,150,86))
        white_field.fill((238,238,210))

        move_indicator = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//8)).convert_alpha()
        move_indicator.fill([90, 30, 30, 120])


        for i in range(8):
            for j in range(0, 8, 2):
                self.screen.blit(white_field, (SCREEN_WIDTH//8*(j+i%2), SCREEN_HEIGHT//8*i))

        for move in self.possible_moves:
            self.screen.blit(
                move_indicator, 
                (SCREEN_HEIGHT//8*(move[1]), SCREEN_WIDTH//8*(7 - move[0]))
            )
        
    def loop(self):
        self.set_board()

        for piece in self.engine_board.board.pieces:
            piece_image = self.pieces_gui.get_image(piece.type, piece.color)

            # height - rows
            # width - colums, but they have to be inverted
            self.screen.blit(piece_image, (
                SCREEN_HEIGHT//8*(piece.position[1]) + (SCREEN_HEIGHT//8 - piece_image.get_height())//2,
                SCREEN_WIDTH//8*(7 - piece.position[0]) + (SCREEN_WIDTH//8 - piece_image.get_width())//2, 
                ))
        
        ev = pygame.event.get()

        # proceed events
        for event in ev:

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                log.debug(pos)
                col, row = pos[0]//(SCREEN_WIDTH//8), (7 - pos[1]//(SCREEN_HEIGHT//8))
                log.debug(f"{col}, {row}")
                for piece in self.engine_board.board.pieces:
                    if piece.position[0] == row and piece.position[1] == col:
                        log.debug(f"Piece {piece.type} {piece.color} pressed")
                        self.piece_pressed = piece

                        self.possible_moves = piece.get_all_moves(self.engine_board.board)
                        log.info(f"Possible moves: {self.possible_moves}")
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.piece_pressed:
                    pos = pygame.mouse.get_pos()
                    col, row = pos[0]//(SCREEN_WIDTH//8), (7 - pos[1]//(SCREEN_HEIGHT//8))

                    log.debug(f"{col}, {row}")
                    self.engine_board.make_move(self.piece_pressed.position, (row, col))
                    # self.piece_pressed.x = col
                    # self.piece_pressed.y = row
                    self.piece_pressed = None
                    self.possible_moves = []
                
            
        pygame.display.flip()
            

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    chess_engine_board = Board()
    pieces_gui = PieceGUI(0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    
    board_gui = BoardGui(screen, chess_engine_board, pieces_gui)
    board_gui.run()


if __name__ == '__main__':
    main()
