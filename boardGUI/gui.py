import logging
from time import sleep

import pygame

# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level = logging.INFO)
log = logging.getLogger(__name__)


from chessEngine.chessEngine import Board
from chessEngine.common import PieceColor, PieceType

from .piece import PieceGUI


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class BoardGui:
    def __init__(self, screen, engine_board, pieces_gui) -> None:
        self.screen = screen
        self.running = True
        self.engine_board: Board = engine_board
        self.pieces_gui: PieceGUI = pieces_gui
        self.piece_pressed = None
        self.possible_moves: list[tuple[int, int]] = []
        self.choosing_promotion: bool = False
        self.promotion_square: tuple[int, int]

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
    
    def draw_promotion_box(self):
        pygame.draw.rect(self.screen, (220,220,220), pygame.Rect(SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-50, 400, 100))
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-50, 400, 100), 5)

        color = self.engine_board.next_move

        self.screen.blit(self.pieces_gui.get_image(PieceType.QUEEN, color), (
                SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-50
                ))
        self.screen.blit(self.pieces_gui.get_image(PieceType.ROOK, color), (
                SCREEN_WIDTH//2-200+100, SCREEN_HEIGHT//2-50
                ))
        self.screen.blit(self.pieces_gui.get_image(PieceType.BISHOP, color), (
                SCREEN_WIDTH//2-200+200, SCREEN_HEIGHT//2-50
                ))
        self.screen.blit(self.pieces_gui.get_image(PieceType.KNIGHT, color), (
                SCREEN_WIDTH//2-200+300, SCREEN_HEIGHT//2-50
                ))
        
    def loop(self):
        self.set_board()

        for piece in self.engine_board.board.pieces:
            piece_image = self.pieces_gui.get_image(piece.type, piece.color)

            # height - rows
            # width - colums, but they have to be inverted
            self.screen.blit(piece_image, (
                SCREEN_HEIGHT//8*(piece.position.col) + (SCREEN_HEIGHT//8 - piece_image.get_height())//2,
                SCREEN_WIDTH//8*(7 - piece.position.row) + (SCREEN_WIDTH//8 - piece_image.get_width())//2, 
                ))
        
        ev = pygame.event.get()
        # self.engine_board.bot_move()
        # sleep(1)
        # proceed events
        for event in ev:
            if self.choosing_promotion:
                if event.type != pygame.MOUSEBUTTONDOWN:
                    continue
                pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH//2-200 < pos[0] < SCREEN_WIDTH//2+200 and SCREEN_HEIGHT//2-50 < pos[1] < SCREEN_HEIGHT//2+50:
                    figure_id = 7 - pos[0]//(SCREEN_WIDTH//8)
                    print(f"IN, CHOOSEN {PieceType(figure_id)}")
                    col, row = self.promotion_square[0]//(SCREEN_WIDTH//8), (7 - self.promotion_square[1]//(SCREEN_HEIGHT//8))
                    self.engine_board.make_move(self.piece_pressed.position, (row, col), PieceType(figure_id))
                    self.choosing_promotion = False
                    self.piece_pressed = None
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.choosing_promotion:
                pos = pygame.mouse.get_pos()
                log.debug(pos)
                col, row = pos[0]//(SCREEN_WIDTH//8), (7 - pos[1]//(SCREEN_HEIGHT//8))
                log.debug(f"{col}, {row}")
                for piece in self.engine_board.board.pieces:
                    if piece.position.row == row and piece.position.col == col:
                        log.debug(f"Piece {piece.type} {piece.color} pressed")
                        self.piece_pressed = piece
                        # print(self.engine_board.next_move)
                        self.possible_moves = piece.get_all_moves(
                            self.engine_board.board, self.engine_board.next_move)
                        log.debug(f"Possible moves: {self.possible_moves}")
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.piece_pressed:
                    pos = pygame.mouse.get_pos()
                    col, row = pos[0]//(SCREEN_WIDTH//8), (7 - pos[1]//(SCREEN_HEIGHT//8))

                    log.debug(f"{col}, {row}")
                    if self.engine_board.make_move(self.piece_pressed.position, (row, col)) == 2: # promotion
                        self.choosing_promotion = True
                        self.promotion_square = pos
                    # self.piece_pressed.x = col
                    # self.piece_pressed.y = row
                    else:
                        self.piece_pressed = None
                    self.possible_moves = []
        if self.choosing_promotion:
            self.draw_promotion_box()
            # pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(30, 30, 60, 60))
            
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
