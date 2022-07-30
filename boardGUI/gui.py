import pygame

from piece import Piece

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

pieces: list[Piece] = []


def reset_pieces():
    for i in range(8):
        pieces.append(
            Piece(i, 1, "black_pawn", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
        )
        pieces.append(
            Piece(i, 6, "white_pawn", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
        )
    pieces.extend([
        Piece(0, 0, "black_rook", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(7, 0, "black_rook", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.extend([
        Piece(0, 7, "white_rook", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(7, 7, "white_rook", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.extend([
        Piece(1, 0, "black_knight", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(6, 0, "black_knight", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.extend([
        Piece(1, 7, "white_knight", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(6, 7, "white_knight", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.extend([
        Piece(2, 0, "black_bishop", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(5, 0, "black_bishop", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.extend([
        Piece(2, 7, "white_bishop", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
        Piece(5, 7, "white_bishop", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8),
    ])
    pieces.append(
        Piece(3, 0, "black_queen", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    )
    pieces.append(
        Piece(3, 7, "white_queen", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    )
    pieces.append(
        Piece(4, 0, "black_king", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    )
    pieces.append(
        Piece(4, 7, "white_king", 0.9*SCREEN_WIDTH//8, 0.9*SCREEN_HEIGHT//8)
    )


def set_board(screen):
    white_field = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//8))

    white_field.fill((238,238,210))
    for i in range(8):
        for j in range(0, 8, 2):
            screen.blit(white_field, (SCREEN_WIDTH//8*(j+i%2), SCREEN_HEIGHT//8*i))
    


def loop(screen):
    set_board(screen)

    for piece in pieces:
        screen.blit(piece.image, (
            SCREEN_WIDTH//8*piece.x + (SCREEN_WIDTH//8 - piece.image.get_width())//2, 
            SCREEN_HEIGHT//8*piece.y + (SCREEN_WIDTH//8 - piece.image.get_height())//2
            ))
    
    pygame.display.flip()
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((118,150,86))
    
    running = True

    reset_pieces()

    while running:
        loop(screen)


if __name__ == '__main__':
    main()
