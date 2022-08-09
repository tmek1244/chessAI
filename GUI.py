import pygame

from boardGUI.gui import BoardGui
from boardGUI.piece import PieceGUI
from chessEngine.chessEngine import Board

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    chess_engine_board = Board()
    pieces_gui = PieceGUI(0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    
    board_gui = BoardGui(screen, chess_engine_board, pieces_gui)
    board_gui.run()


if __name__ == '__main__':
    main()
