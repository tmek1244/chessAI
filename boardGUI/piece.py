import os
import pygame
from enum import Enum

from chessEngine.common import PieceType, PieceColor


class PieceGUI(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # self.surf = pygame.Surface((width, height))
        # self.surf.fill((120, 120, 120))
        # self.rect = self.surf.get_rect()

        self.images = {}
        for piece_type in PieceType:
            for piece_color in PieceColor:
                type_str = {
                    PieceType.PAWN: 'pawn',
                    PieceType.ROOK: 'rook',
                    PieceType.KNIGHT: 'knight',
                    PieceType.BISHOP: 'bishop',
                    PieceType.QUEEN: 'queen',
                    PieceType.KING: 'king'
                }[piece_type]
                color_str = {
                    PieceColor.BLACK: 'black',
                    PieceColor.WHITE: 'white'
                }[piece_color]
                base_path = os.path.dirname(__file__)
                piece_path = os.path.join(base_path, f'images/{color_str}_{type_str}.png')
                self.images[(piece_type, piece_color)] = pygame.transform.scale(
                    pygame.image.load(piece_path),
                    (width, height)
                )

    def get_image(self, piece_type: PieceType, piece_color: PieceColor):
        return self.images[(piece_type, piece_color)]
